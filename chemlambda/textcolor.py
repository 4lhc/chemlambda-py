# -*- coding: utf-8 -*-
#
#  textcolor.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Wed 28 May 2014 15:31:41 IST
#  ver    : 

# coloured text output, print messages


class TextColor(object):
    """colored text outputs and lines

    functions          :    ftext(), hr(), esctext()

    attributes         :    normal
                            red, green, yellow, blue, magenta, cyan
                            r, g, y, b, m, c
                            bold colours -
                            RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN
                            R, G, Y, B, M, C

    colournames        :    accepted values "red", "green", "yellow", "blue",
                            "magenta", "cyan" and "white"
                            also short names "rd", "gr", "ye", "bl", "mg",
                            "cy" and "wt"

                            hr() accepts comma delimited multiple colors eg "rd, gr, cy"

    text attributes    :    accepted values "bold" (default), "none", "italics",
                            "uline", "blink" and "inv"
                            multiple options need to be comma seperates
                            eg: "bold, italics, blink"
    """
    """ Basic color escape sequence """
    _r = _red = '\033[2;91m'
    _g = _green = '\033[2;92m'
    _y = _yellow = '\033[2;93m'
    _b = _blue = '\033[2;94m'
    _m = _magenta = '\033[2;95m'
    _c = _cyan = '\033[2;96m'

    #bold
    _R = _RED = '\033[1;91m'
    _G = _GREEN = '\033[1;92m'
    _Y = _YELLOW = '\033[1;93m'
    _B = _BLUE = '\033[1;94m'
    _M = _MAGENTA = '\033[1;95m'
    _C = _CYAN = '\033[1;96m'

    _E = _END = '\033[0m'
    
    
    def __init__ (self):
        """"""
        self._er_col = "red"
        self._wn_col = "yellow"
        self._in_col = "blue"
        self._ok_col = "green"
        pass


    def esctext(self, col, fattr = "bold"):
        """
        create escape sequence for input colour and style
        Arguments
        --------------
        col (str)           :   colour names
                                accepted values- see colournames in class docstring
        fattr (str)         :   text styles
                                accepted values- see text attributes in class docstring

        Returns
        --------------
        str                 :   the escape sequence

        Raises
        --------------
        KeyError

        """
        style_dict = { #colours
                        "red": "91", "rd": "91",
                        "green": "92", "gr": "92",
                        "yellow": "93", "ye": "93",
                        "blue": "94", "bl": "94",
                        "magenta": "95", "mg": "95",
                        "cyan": "96", "cy": "96",
                        "white": "97", "wt": "97",
                       #styles
                        "bold": "1",
                        "none": "2",
                        "italics": "3",
                        "uline": "4",
                        "blink": "5",
                        "inv": "7"
                     }
        try:
            styles = ";".join([style_dict[i.strip()] for i in fattr.split(",")])
        except KeyError:
            print("Warning: KeyError, style set to default")
            styles = "bold"

        tcolor = style_dict[col]
        return "\033[{};{}m".format(styles, tcolor)


    def hr(self, hr_len=30, hr_col="yellow", hr_char = "-", hr_attr = "bold" ):
        """
        create a horizontal rule of specified length
        Arguments
        --------------
        hr_len (int)        :   length of the hr (default: 30)
        hr_col (str)        :   see colournames in class docstring
                                comma delimited multiple colors supported
                                (default: 'yellow')
                                eg "rd, gr, cy"
        hr_char (str)       :   character to be used (default: '-')
        hr_attr (str)       :   see text attributes in class docstring

        Returns
        --------------
        str

        Raises
        --------------

        """
        hr_colors = [i.strip() for i in hr_col.split(",")]
        hr_len_per, remainder = divmod(hr_len, hr_colors.__len__())
        hr_dict = {}
        hr_l = ""
        for hc in hr_colors:
            if remainder > 0:
                hrlen = hr_len_per + 1
                remainder -= 1
            else:
                hrlen = hr_len_per
            hr_l += "{}{}".format(self.esctext(hc, hr_attr), hr_char*hrlen)
        hr_l += self._END
        return hr_l


    def ftext(self, ftext, fcol, fattr = "bold" ):
        """
        wrap escape sequence around the input text

        Arguments
        --------------
        ftext (str)         :   input text
        fcol (str)          :   colour names
                                accepted values- see colournames in class docstring
        fattr (str)         :   text styles
                                accepted values- see text attributes in class docstring

        Returns
        --------------
        str : text wrapped with escape sequences

        Raises
    """ 
        return "{}{}{}".format(self.esctext(fcol, fattr), ftext, self._END )

    def warn(self, wtext, wattr = "bold"):
        """
        Print a warning message

        Arguments
        --------------
        wtext (str)     :   the message to be printed
        wattr (str)     :   as per colour specifications of TextFormat class

        Returns
        --------------
        None

        Raises
        --------------

        """
        _warning =  self.ftext("Warning:", self._wn_col, wattr)
        _wmsg = "{} {}".format(_warning, wtext)
        print(_wmsg)


    def error(self, etext, eattr = "bold"):
        """
        Print an error message

        Arguments
        --------------
        etext (str)     :   the message to be printed
        eattr (str)     :   as per colour specifications of TextFormat class

        Returns
        --------------
        None

        Raises
        --------------

        """
        _error = self.ftext("Error:", self._er_col, eattr)
        _emsg = "{} {}".format(_error, etext)
        print(_emsg)


    def info(self, itext, iattr = "bold"):
        """
        Print an info message

        Arguments
        --------------
        itext (str)     :   the message to be printed
        iattr (str)     :   as per colour specifications of TextFormat class


        Returns
        --------------
        None

        Raises
        --------------

        """
        _info = self.ftext("Info:", self._in_col, iattr)
        _imsg = "{} {}".format(_info, itext)
        print(_imsg)


    def okay(self, otext, oattr = "bold"):
        """
        Print an info message

        Arguments
        --------------
        itext (str)     :   the message to be printed
        iattr (str)     :   as per colour specifications of TextFormat class


        Returns
        --------------
        None

        Raises
        --------------

        """
        _okay = self.ftext("OK:", self._ok_col, oattr)
        _omsg = "{} {}".format(_okay, otext)
        print(_omsg)


def main():

    return 0

if __name__ == '__main__':
    main()

