import healpy as hp
from threeML.plugin_prototype import PluginPrototype
from astromodels import Uniform_prior, Cosine_Prior
import collections



_allowed_coords = ['C', 'G']

class HEALPixMapLike(PluginPrototype):

    def __init__(self, name, healpix_map, coord='C'):
        """
        A plugin for healpix probability maps. Allows for joint fitting 
        of positions on the sky. Coordinate system is assumed to be Celestial.
        this can be changed in the future. 

        :param name: plugin name
        :param healpix_map: a healpix map array
        :param coord: the coordinate system of the map: G or C
        :returns: 
        :rtype: 

        """


        assert coord.upper() in _allowed_coords, 'coord must be G or C'

        self._coord = coord.upper()
        
        self._map = healpix_map

        # the map should be filled with probabilities
        # and we will be using the log of them. Let's
        # go ahead and do that

        self._log_map = np.log(healpix_map)

        # create the hash for the nuisance parameters
        nuisance_parameters = collections.OrderedDict()

        # call the prototype constructor
        super(HEALPixMapLike, self).__init__(name, nuisance_parameters)

    def set_model(self, model):
        """
        Sets the likelihood model for the plugin

        :param model: 
        :returns: 
        :rtype: 

        """

        # attach the model to the object
        self._likelihood_model = model

        # the position for the point source is freed
        for key in self._likelihood_model.point_sources.keys():
            self._likelihood_model.point_sources[key].position.ra.free = True
            self._likelihood_model.point_sources[key].position.dec.free = True

        # set proper priors for the coordinates
        self._likelihood_model.point_sources[key].position.ra.prior = Uniform_prior(lower_bound=0., upper_bound=360)
        self._likelihood_model.point_sources[key].position.dec.prior = Cosine_Prior(lower_bound=-90., upper_bound=90)

    def get_log_like(self):

        # assume only one point source


        if self._coord == 'C':
        
            org = 0.
            # get the ra, dec from the model
            ra, dec = self._likelihood_model.get_point_source_position(0)

            y = dec
            # healpix has normal coordinates, so fix ours
            x = np.remainder(ra + 360 - org, 360)
            if x > 180.:
                x -= 360
            x = -x

        else:

            ## add here getting the l,b
            pass

        # 
        return hp.get_interp_val(self._log_map, x, y, lonlat=True)

    def inner_fit(self):

        return self.get_log_like()

    @classmethod
    def from_healpix_file(cls, name, filename, **kwargs):
        """
        Construct a HEALPixMapLike from a file name

        :param name: plugin name
        :param filename: healpix FITS filename
        :returns: 
        :rtype: 

        """
        

        hp_map = hp.read_map(filename, **kwargs)

        return cls(name, hp_map)
