#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
#-----------------------------------------------------------------------------
import os
import sys
import inspect
import datetime
from dbms import DBMS
from tools import Tools

class Engine(DBMS, Tools):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"

    def __str__(self):
        return "class: {0}\nMRO:{1}".format(self.__class__.__name__,
                       [x.__name__ for x in Engine.__mro__])


    def get_file(self, file):
        """# return full path of the directory where program resides."""

        return os.path.join(os.path.dirname(__file__), file)

    def on_log(self, container, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n{1}\n{2}\n{3}\n{4}\n\n".format(now, function, exc_value, exc_type, module)
        log_file = open("log.txt", "a")
        log_file.write(log_text)
        log_file.close()


    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]

            return d
        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_icon(self):
        return """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/A
                  P+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1goLDgY06HK0Cw
                  AAAuNJREFUSMfNldlL1UEUx78zv9/vru5ilt5K73WJVCQSizZRCvVGUohKlOB
                  L9BZEPURU9FIa/QVB79FCSEK9ZEVFUE8JZYHbTS1zverdfsvM/HoxMfVuFdGB
                  8zRzzuecM9+ZAf4vM0myEQkHeLydHSal5ym37xx8ckb7q4CtjZ11iiI9zslOo
                  zOzgbchM1Rv4dbQyj1UJxnDTy8srI6l8ZK7vV0Vkiw9Ot5cYz3dXq+UlLiqnD
                  TlOQBcOtuCK+faIEk0akcxAUWNN1xEps+ONOxy5OVmwzcVwrGGatv2bVsqAUC
                  RJUg09hDkqJUf7Eo3FfJi3+7yjLJiFxn8HgDjJkanTTQdqrLmZqWACzPujNfv
                  oOWeJDml7sqygvwD1aXyyFQQjJsAgKDKMDQZhLuoECNTIZhxAOt2UKz7bm/Oy
                  6mur9lhG5pYRDDCflk3DIZASAOlBJzbwbmwEhspANC3Ope0Ro5NNy9npKeeaj
                  u6xzk+G8ZcUAMXYl1nXCDdoSAtLUX4RidbMz213f6B3tmoMi30Xm+32W23Otr
                  q7Isqw4Q/ElfCFpmiND8d/QNfRe/LvnkBttfXc/Hzmg62NnbWSRb5zonm/Xan
                  04ZPY/6ola90nXHMBlRUFucSq81qHRubOZnqqe1ZGOydXj5kt7erghD0coPb7
                  z58BVVjYEzAMHhCHlEZVI3h9ZsPlHOeSQn56Dl8rXz5kFVJHZKFNQsAwqoxp+
                  kGGGPgwkzoOZAoQURnMBiHIMgCgIhh0ZcB33quhgGEAaDA27m0OXGAoAQRzQA
                  Ac9ThWcT9Vh5TphFVh24kDgAAXWcglOhu/3DKMLAQG6AZ0A0GkQQgrOmJX7SQ
                  qkNnyQKMJdWbMQGbAEDTOTgTEGbiAFVjgGnS6f4HGxFlRBkAXADAhMCGTEdSH
                  4fBOAgFjPB0HoBJAPOrAeRnnvfv+n/3T1UUZ7ZTnf9CohXmAuCI9YzHMbYk9/
                  FYnRP8mZn4l/YD7TuA32k81GAAAAAASUVORK5CYII="""

    def get_exit__icon(self):
        return """iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIf
                  AhkiAAAAAlwSFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lm
                  lua3NjYXBlLm9yZ5vuPBoAAAO5SURBVDiNjZXPax1VFMc/996ZO/N+mKZ5TYo
                  +QmNMhLYhpZJVC7pojLgLtCItajFYwY102RQENyFCcVP1H6iIiF25EFwli0q6
                  aFpcNNBSXsEarPASXybv550f18X74XvJC3rgMMPM4TPfe+b8ENZa/ocJQAJO6
                  wpggQiIW/c95gC898GlJWPM9YOoSinS6TQDA4fwPQ+AMApxXX1zeemLa0B9L9
                  wBMMZcf+f8uxQKBarVKrVajVqthjEGYwxSSqanprly5SOkbAqu12t89c3XnwJ
                  LgGkp7wUDeJ6H1powDImiiDiOSZIEAK01Q0NDKKVQSgGQTmcYGR4GSAPbfVMB
                  4Ps+WmuiKCJJEtq5N8bgeR6ZTAYhJEI0FQsBWns9jL5grTW+7/dAhRBIKdFa4
                  7Vy222ttIh+YNkd5DgOnufh+z6+7+N5Xse11oi+CPghm33jeyFu9VUspey4Ug
                  rHcZiYmCCOY4rFIq7r9oX+PD198fDU1PXg0SP1nRAftx5HHcXtY3f75uYmvu8
                  zOTnZ+Wlts0mCc+tbsvn84mtXr3pKqUgqVZaOUxZQ7En8XrC1lkKhwKlTpzDG
                  dOLCIODO/Dzjw8OMnz3r21KJ12/c8Nvvf1lY8HvAe1VnMhlmZma4e/cux48fB
                  6Dy9Cmrc3OMzswwPDrK7soKWItQCpskDMzOIqRkn2IhROcDJ06c4NmzZ5RKJV
                  KpFAC/XrjAkZERBn2f3dVVbBSRVCoklQoylSJ18iQIwYGK8/k81WqVhw8fks1
                  mcZxm6OmbN7kzP49jDC8A9Y0NbKuRABpPnmDjeH9xt8FbW1vs7OyQTqfRWgOQ
                  JAlHzpzhzbU1Vs6d43A2w9HTp5EDA82OUYq4WgX6dE0bHIZhp8SklBQKBaSUj
                  I2NkXtlnNl79/jp7Bnqm5v1Ucfxf1tbM/bfvvhbHgTurmfHcSiVSuwEO1QqZe
                  I4Rg0eorF4jXKttvJ4Y6NmIblkrdvyF/eB23ClFFprisUi6/fX0Z4m/1KeXC5
                  HFEUYY6iaBue3tz+plctfCnjczeg7QLTWBEHA+vo9Xh4f4/Ll9zl2bKw5/aKQ
                  MAqJ45hgdxegcTGKPgc+6wu21qKUwlrLgwf3OTQ4wIcLl8nlcriuSxyH1OoRA
                  rAWkiQmCAKABgdtkDiOkVLy/K/nCCxvvT1HKuXjum5z2IdhzwizNFv6P8HBTs
                  Aff/7OxKvN4yIsjUadhmk0gR2q6DCSxFKplKG5PfqDR46OLN/+8fZid+eJg2Z
                  kV+q01svsWUlt+wfnpXqRmhuUSQAAAABJRU5ErkJggg=="""

    def get_info_icon(self):
        return """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIf
                  AhkiAAAAAlwSFlzAAAK6wAACusBgosNWgAAABh0RVh0U29mdHdhcmUAQWRvYm
                  UgRmlyZXdvcmtzT7MfTgAAABZ0RVh0Q3JlYXRpb24gVGltZQAwMy8wNC8wOK6
                  M4pgAAAXDSURBVEiJjZVbjFXVGcd/a6+1z23OGRjU6cyRYxVmEC0FIqONYOgo
                  EiMXY1NNL2m0fai+VPpEeGjaGJM++YZ9qDzRPtResKGR4gNaKC1ptEhpq7UMl
                  7Yg58xwmcuZfc7ee137MMPYSiD+k/W0vu/7fd/OXt9fhBC4mUTlmVG1ac3zjf
                  7ebaWCqhIgMza5cGnmgH3776+G7k+O3DT/RgCx7nubR0Y/98Lm+5ZtWLXsM32
                  Dt9ZEsRBDgFQbWldmwwfnJqYOnTh37L2jH7wSjv/w0KcCCPFEX/2ZrXu+tXXd
                  U4994W6qtQqJdmjj8QH8fHxBRVQLkk6ny6F3xth78L19zZ8efC6E30zdECAGv
                  t1Y+9XRt7779S+uqNdvY3w6RQgoxZKSkvSUC1gXmE1zcuPIjMMD9cVlWq0r/O
                  jnR8dO/vL3j4bmngvXAYR4YtHqHV85/p1vPDLk4hKd3FApSIpKUo4lCMGps02
                  cDwzdNQgEMm3JraejHT0lRWw1P/7Z7878bfe+kRD2zwCoa6Slz27bu/2x+4da
                  OsJ0ulRiCQisB0vEh++P8eXP9yOAX/x1jBX3DqGNJzce7TzTUylxLHl88/1DV
                  2c6e4EvAUQA6pGXHl6zdvjJrFRlfDolNZ5Z7ZnVjo7xnG5Nc88tRR5a1WDDqg
                  arbi1xpjVNx3gS7ZjNHV3jGJ9O6RQqrF49/GS86aWHFyZorLhjZ3VwgPNXEsq
                  xxPhAMQ4UbERmA1Ecc/J8wuXJNgQ40UzoaSxhOrVo68itI7ee3DgudxJq/f00
                  hho7gcOisH7XxpWj69+o33t3r3eWUjz33YtKUlARBRUhpGRiMmGmNQHAwGdvp
                  69aopsbtPPo+eKZdWjjKAlB89SZ9j+Ovbtd1eoDO0Jc6p1upwQpyGygqDyF2F
                  NUEuc89vw5HlwxgF22GHzg5MWLZAO3QwjzE1wDeLyxaOtBFXtrg/07lBFqi7G
                  CTpJhY4WMPWUVEWsPkcV6GO9Inu3v4en1wwDsfO3P/Ppim1sqMYRACAHtPFY7
                  hNZoYzEWLHKLSm0o57nFJBmuEKOlJA8CGwIgkDJiRvZy+PQkT6+f++MS7Th3V
                  XM5UTjvCSFQFFDFU3SOSBt8aklNKCsXSdLUEJygi6YrIpxSEEuUksTS4zKDEM
                  WFBxkCYByZFFjrCcaRakPHWip4erwDY3CRRBVLKk1SUw4dgy3EyIJCeI8PCus
                  9Noogt3hfWAA4HyA3GAGRtUjriIwlMgatLT7XCCUolgtp1BOHg4aAzDRKG2Q+
                  d1SmUWmOzDRker7teXkPqUalGSrTyFwjtZ7Lm6+hhaBS4GC0pD2xO8RRO0LMB
                  eYamefIPEflGpnlkGZzRa/tF+8hnb/Pc2Q218i1/AhBKMr2ktnx3dGp139wVP
                  rsmK5VUbOduaBs/qQ5Kssh1eA+BgTnIcuJPllYG1TSIV/cSxTyY2O/+v7RCGD
                  J1Qsv51UFlR5U0p2H5MhcozIN0wkVJRYAPbGE6YQ40x93n2lU0iVUqmS1mCWT
                  F15e2EUfvb7rcHny4v6ZZUuJgiBOOgsTmJkOa5YX2TLSoDmV0JxK2DqylLVDJ
                  Uy7i8zMQvEIwczwHZSnWvs/2rfr8P+t620PfG3R22u3H7cDy4f6/vI+sj2LK5
                  exQlCtSYIQZNoCUC4oCIFO2yBDQHZSfG+NyXWrURNnz2w6+cbIgXdfm7nOcO4
                  b3dH4cPiBt3Rj5Yraf1pUTp8F5/BK4aI5T4AAPiC9RxoNUtIdHqJ9V53ChVNj
                  95x+59ETR3ZfbzjXtHXjN/uONh7c071z5VNRsUaldYlicxzZThDWQIAQx7hal
                  bw+QHfwNrxJqPzrn/s2nv/Tc7/9w94bW+b/qv74i5tn6stfyPrrG0K51ieEFG
                  I+NghBCC6IdHaqdKl5bFHz7CvNN1/8dKb/SS17aMdoOnjn8+24Z1s3iqsAFW+
                  SXtM5UG79+9Vzf9x95Gb5/wVqoFAAkdjM6AAAAABJRU5ErkJggg=="""


def main():
    #testing some stuff
    foo = Engine()
    print(foo)
    print(foo.set_connection())
    input('end')

if __name__ == "__main__":
    main()
