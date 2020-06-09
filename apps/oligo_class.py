
class oligo():
    """Functions for characterization of site-directed mutagenesis primers"""
    def __init__(self, primer):
        self._primer = self.prep(primer)

    def prep(self, primer):
        """
        Function will provide a string value in all lowercases while removing all spaces

        :param primer: Input primer sequence in string format
        :return: Primer in string format without spaces and all lowercase letters
        """
        self._primer= ''.join(primer.split())
        self._primer= self._primer.lower()
        return(self._primer)

    def comp(self):
        """
        Function will calculate total number of GC bases

        :param primer: Input primer sequence in string format
        :return: Integer value of total number of GC bases
        """
        GC= 0
        for i in self._primer:
            if i in 'gc':
                GC += 1
        return GC

    def F_lockdown(self):
        """
        Function will provide boolean answer to whether primer ends in GC pair

        :param primer: Input primer sequence in string format
        :return: Boolean answer to whether primer terminates with GC
        """
        if self._primer[-1] in 'gc':
            return True
        else:
            return False

    def R_lockdown(self):
        """
        Function will provide boolean answer to whether primer begins with G or C

        :param primer: Input primer sequence in string format
        :return: Boolean answer to whether primer begins with G or C
        """
        if self._primer[0] in 'gc':
            return True
        else:
            return False

    def content(self):
        """
        Calculates percentage content of GC in primer

        :param primer: Input primer sequence in string format
        :return: Float value of GC%
        """
        # primer = self._primer
        # print(primer)
        gc = oligo(self._primer).comp()
        size = len(self._primer)
        gc_content = round(gc / size * 100)
        return gc_content


    def Tm_temp(self, mutations):
        """
        Calcualtes Tm using Strategene site-directed mutagenesis formula

        :param primer: Input primer sequence in string format
        :param mutations: Integer value representing total number of mutations to create
        :return: Float value represent Tm (in C) of primer
        """
        self._mutations = mutations
        gc_content = oligo(self._primer).content()
        Tm= 81.5 + ((0.41 * gc_content) - ((675 / (len(self._primer))) - self._mutations))
        Tm = round(Tm, 1)
        return Tm

if __name__ == "__main__":
    primer = 'ATGgcgcgcgcgcgcgccc'
    mutations = 2

    seq = oligo(primer)
    print(seq._primer)
    print('Comp', seq.comp())
    print('R', seq.R_lockdown())
    print('F', seq.F_lockdown())
    print('Content', seq.content())
    print('TM', seq.Tm_temp(mutations))