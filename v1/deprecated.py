
def koppen_kottek(index):
    #pre-calculations
    Tann = ts[index].sum() / 12
    Pann = pr[index].sum()
    koppenClass = "G"
    if ts[index].max() < 10:  # E
        if ts[index].max() < 0:
            koppenClass = "EF"
        else:
            koppenClass = "ET"
    else:
        # we need to separate the hemispheres because their summer and winter months differ
        if index < rows * cols / 2:  # southern hemisphere, winter from the 3rd to 9th month
            he = "S"
            if pr[index, 3:9].sum() > 2 * Pann / 3:
                Pth = 2 * Tann
            elif numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() > 2 * Pann / 3:  # summer
                Pth = 2 * Tann + 28
            else:
                Pth = 2 * Tann + 14
        else:  # northern hemisphere, summer from the 3rd to 9th month
            he = "N"
            if numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() > 2 * Pann / 3:
                Pth = 2 * Tann
            elif pr[index, 3:9].sum() > 2 * Pann / 3:  # summer
                Pth = 2 * Tann + 28
            else:
                Pth = 2 * Tann + 14

        if Pann < 10 * Pth:  # B
            if Pann > 5 * Pth:
                koppenClass = "BS"
            else:
                koppenClass = "BW"
        else:
            if ts[index].min() >= 18:  # A
                Pmin = pr[index].min()
                if Pmin >= 60:
                    koppenClass = "Af"
                else:
                    if Pann >= 25 * (100 - Pmin):
                        koppenClass = "Am"
                    else:
                        if he == "N":
                            if pr[index, 3:9].min() < 60:  # Northern summer
                                koppenClass = "As"
                            elif numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() < 60:
                                koppenClass = "Aw"
                        elif he == "S":
                            if numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() < 60:  # Southern summer
                                koppenClass = "As"
                            elif pr[index, 3:9].min() < 60:
                                koppenClass = "Aw"
            else:
                if he == "N":
                    Psmin = pr[index, 3:9].min()
                    Psmax = pr[index, 3:9].max()
                    Pwmin = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).min()
                    Pwmax = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).max()
                elif he == "S":
                    Pwmin = pr[index, 3:9].min()
                    Pwmax = pr[index, 3:9].max()
                    Psmin = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).min()
                    Psmax = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).max()

                if ts[index].min() <= -3:  # D
                    if Psmin < Pwmin and Pwmax > 3 * Psmin and Psmin < 40:
                        koppenClass = "Ds"
                    elif Pwmin < Psmin and Psmax > 10 * Pwmin:
                        koppenClass = "Dw"
                    else:
                        koppenClass = "Df"
                else:  # C
                    if Psmin < Pwmin and Pwmax > 3 * Psmin and Psmin < 40:
                        koppenClass = "Cs"
                    elif Pwmin < Psmin and Psmax > 10 * Pwmin:
                        koppenClass = "Cw"
                    else:
                        koppenClass = "Cf"

    if koppenClass[0] == "B":
        if Tann >= 18:
            koppenClass = koppenClass + "h"
        else:
            koppenClass = koppenClass + "k"

    if koppenClass[0] == "C" or koppenClass[0] == "D":
        if ts[index].max() >= 22:
            koppenClass = koppenClass + "a"
        else:
            T10mon = 0
            for temp in ts[index]:
                if temp > 10:
                    T10mon += 1
            if T10mon >= 4:
                koppenClass = koppenClass + "b"
            else:
                if ts[index].min() > -38:
                    koppenClass = koppenClass + "c"
                else:
                    koppenClass = koppenClass + "d"

    koppenDict = {
        "Af": 1,
        "Am": 2,
        "Aw": 3,
        "BWh": 4,
        "BWk": 5,
        "BSh": 6,
        "BSk": 7,
        "Csa": 8,
        "Csb": 9,
        "Csc": 10,

        "Cwa": 11,
        "Cwb": 12,
        "Cwc": 13,
        "Cfa": 14,
        "Cfb": 15,
        "Cfc": 16,
        "Dsa": 17,
        "Dsb": 18,
        "Dsc": 19,
        "Dsd": 20,

        "Dwa": 21,
        "Dwb": 22,
        "Dwc": 23,
        "Dwd": 24,
        "Dfa": 25,
        "Dfb": 26,
        "Dfc": 27,
        "Dfd": 28,
        "ET": 29,
        "EF": 30,

        "As": 31,
        "G":0
    }

    return koppenDict[koppenClass]


def coffee(index):
    MAT = ts[index].sum() / 12
    Tcold = ts[index].min()
    if 1125 < pr[index].sum() < 1875:
        if 17 < MAT < 24 and Tcold > 7:
            return 1
        else:
            return 0
    else:
        return 0
