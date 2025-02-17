from .healpix_map_like import HEALPixMapLike



class LIGOMapLike(HEALPixMapLike):

    def __init__(self, name, ligo_map, **kwargs):

        super(LIGOMapLike, self).__init__(name=name, healpix_map=ligo_map, coord='C')


    @classmethod
    def from_healpix_file(cls, name, bayestar_file):

        return super(LIGOMapLike, cls).from_healpix_file(name=name, filename=bayestar_file)
