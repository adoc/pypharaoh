"""
"""

import os
import binascii
import pyramid.compat
import pyramid.scaffolds
import pyramid.scaffolds.template


class SrbbStack(pyramid.scaffolds.PyramidTemplate):
    """SQLAlchemy, Require, Backbone, Bootstrap
    """
    secret_entropy = 32    # In Bytes
    _template_dir = 'srbb_stack'
    summary = ("Sets up a standard RESTful Pyramid application and front end "
            "using SQLAlchemy, Require.js, Backbone.js, and Bootstrap.")

    @staticmethod
    def _gen_sec(entropy=secret_entropy):
        return pyramid.compat.native_(
            binascii.hexlify(os.urandom(entropy)))

    def pre(self, command, output_dir, variables):
        """Add some additional variables for use as secrets.
        """
        variables['dev_auth_tkt_secret'] = self._gen_sec()
        variables['stage_auth_tkt_secret'] = self._gen_sec()
        variables['prod_auth_tkt_secret'] = self._gen_sec()
        variables['auth_identity_secret'] = self._gen_sec()
        variables['beaker_session_secret'] = self._gen_sec()

        if variables['package'] == 'core':
            raise ValueError('Sorry, you may not name your package "core". '
                             'The package name "core" has a special meaning in '
                             'this scaffold.')

        return pyramid.scaffolds.PyramidTemplate.pre(self, command, output_dir,
                                                     variables)

    def post(self, command, output_dir, variables):

        return pyramid.scaffolds.PyramidTemplate.post(self, command,
                                                        output_dir, variables)
        
        # When creating a custom message return this instead.
        # return pyramid.scaffolds.template.Template.post(self, command,
        #                                                 output_dir, variables)

class ExtendedSrbbStack(SrbbStack):
    """SRBB Stack with separated RESTful API and Front End Framework.
    """

    