import geojson
import osmapi
import shapely.geometry
from alpha_shape import alpha_shape

api = osmapi.OsmApi()


class OsmSite():

    # osm_ref format 'node/nnnnnnnnn', 'relation/nnnnnnn', 'way/nnnnnnn'
    def __init__(self, osm_ref: str):
        self.osm_ref = osm_ref
        if self.osm_ref.startswith('/'):
            self.osm_ref = self.osm_ref[1:]
        self.properties = {}
        self.properties['osm_ref'] = self.osm_ref
        self.generators = None
        try:
            if self.osm_ref.startswith('node/'):
                id = self.osm_ref[self.osm_ref.index('node/') + len('node/'):]
                node = api.NodeGet(id)
                point = self.point_from_node(node)
                buffered_point = point.buffer(0.001)
                self.geom = buffered_point
                self.update(node['tag'])
                if self.is_power_generator(node):
                    point = self.point_from_node(node)
            elif self.osm_ref.startswith('way/'):
                id = self.osm_ref[self.osm_ref.index('way/') + len('way/'):]
                way = api.WayGet(id)
                polygon = self.polygon_from_way(way)
                self.geom = polygon
                self.update(way['tag'])
            elif self.osm_ref.startswith('relation/'):
                id = self.osm_ref[self.osm_ref.index('relation/') + len('relation/'):]
                relation = api.RelationGet(id)
                self.update(relation['tag'])
                points = []
                polygons = []
                for member in relation['member']:
                    if member['type'] == 'node':
                        node = api.NodeGet(member['ref'])
                        if self.is_power_generator(node):
                            point = self.point_from_node(node)
                            points.append(point)
                            # duplicate individual turbines for plotting
                            self.add_generator(
                                geojson.Feature(
                                    geometry=point,
                                    tippecanoe={"maxzoom": 15, "minzoom": 10},
                                    properties=node['tag']
                                )
                            )
                    if member['type'] == 'way':
                        way = api.WayGet(member['ref'])
                        if self.is_power_generator(way):
                            polygon = self.polygon_from_way(way)
                            polygons.append(polygon)
#                            self.add_generator(
#                                geojson.Feature(
#                                    geometry=polygon,
#                                    properties=way['tag']
#                                )
#                            )
                        elif self.is_access_track(way):
                            pass
                        elif self.is_building(way):
                            pass
                        elif self.is_cable(way):
                            pass
                        elif self.is_fence(way):
                            if self.properties['plant:source'] == 'solar':
                                # solar often has a perimeter fence
                                polygon = self.polygon_from_way(way)
                                polygons.append(polygon)
                            else:
                                pass
                        elif self.is_landuse(way):
                            pass
                        elif self.is_substation(way):
                            pass
                        elif member['role'] == 'outer':
                            polygon = self.polygon_from_way(way)
                            polygons.append(polygon)
                        else:
                            if len(way['tag']) == 0:
                                polygon = self.polygon_from_way(way)
                                polygons.append(polygon)
                            else:
                                print(
                                    "not sure what it is {} so ignoring".format(
                                        way
                                    )
                                )
                if len(points) > 1:
                    hull, edge_points = alpha_shape(points)
                    polygons.append(hull)
                elif len(points) == 1:
                    point = points[0]
                    buffered_point = point.buffer(0.001)
                    polygons.append(buffered_point)
                if len(polygons) > 1:
                    self.geom = shapely.geometry.MultiPolygon(polygons)
                else:
                    self.geom = polygons[0]
            else:
                raise Exception(
                    "did not understand osm_ref {}".format(osm_ref)
                )
            # remove unwanted properties
            self.delete('note')
            self.delete('ref')
            self.delete('source')
            self.delete('source:geometry')
            self.delete('source:name')
            self.delete('source:position')
            self.delete('source:ref')
            self.delete('url')
            self.delete('voltage')
            self.delete('website')
            self.delete('wikimedia_commons')
            self.delete('wikipedia')
            
        except Exception as e:
            raise Exception("{} {}".format(osm_ref, e))

    def update(self, properties: iter) -> None:
        self.properties.update(properties)

    def delete(self, key: str) -> None:
        self.properties.pop(key, None)
        # TODO delete from generators too?

    def feature(self) -> geojson.Feature:
        return geojson.Feature(
            geometry=self.geom,
            properties=self.properties
        )

    def feature_collection(self) -> geojson.FeatureCollection:
        boundary = geojson.Feature(
            geometry=self.geom,
            properties=self.properties
        )
        features = []
        if self.generators:
            features = self.generators.features
        features.append(boundary)
        if len(features) == 1:
            return features[0]
        return geojson.FeatureCollection(features)

    def add_generator(self, feature: geojson.Feature) -> None:
        if self.generators is None:
            self.generators = geojson.FeatureCollection(features=[])
        features = self.generators.features
        features.append(feature)
        self.generators = geojson.FeatureCollection(features)

    @staticmethod
    def point_from_node(node) -> shapely.geometry.Point:
        lonlat = (round(node['lon'], 5), round(node['lat'], 5))
        feature = shapely.geometry.Point(lonlat)
        return feature

    @staticmethod
    def polygon_from_way(way) -> shapely.geometry.Polygon:
        coords = []
        for id in way['nd']:
            node = api.NodeGet(id)
            lonlat = (round(node['lon'], 5), round(node['lat'], 5))
            coords.append(lonlat)
        feature = shapely.geometry.Polygon(coords)
        return feature

    @staticmethod
    def is_access_track(way) -> bool:
        found = 'highway' in way['tag'].keys() or 'track' in way['tag'].keys()
        return found

    @staticmethod
    def is_antenna(node) -> bool:
        found = 'antenna' in node['tag'].values()
        return found

    @staticmethod
    def is_building(way) -> bool:
        found = 'building' in way['tag'].keys()
        return found

    @staticmethod
    def is_cable(way) -> bool:
        found = 'cable' in way['tag'].values()
        return found

    @staticmethod
    def is_fence(way) -> bool:
        found = 'barrier' in way['tag'].keys()
        return found

    @staticmethod
    def is_landuse(way) -> bool:
        found = 'landuse' in way['tag'].keys()
        return found

    @staticmethod
    def is_power_generator(node_or_way) -> bool:
        tags = node_or_way['tag']
        power = 'power' in tags
        generator = 'generator' == tags
        power_generator = power and generator
        generator_source = 'generator:source' in tags
        if generator_source == 'wind':
            if 'generator:type' not in tags:
                print(
                    "No generator:type https://www.openstreetmap.org/node/{}"
                    .format(node_or_way['id'])
                )
        elif power_generator:
            print(
                "No generator:source https://www.openstreetmap.org/node/{}"
                .format(node_or_way['id'])
            )
        return generator_source or power_generator

    @staticmethod
    def is_substation(node_or_way) -> bool:
        found = 'substation' in node_or_way['tag'].values()
        return found
