from setuptools import setup
import setup_translate

pkg = 'Extensions.TelekomSport'
setup(name='enigma2-plugin-extensions-telekomsport',
       version='1.0',
       description='Telekom Sport Plugin',
       package_dir={pkg: 'TelekomSport'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
