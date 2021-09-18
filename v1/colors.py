# run in the arcgis python window
# use the wildcards inside m.litlayers
# NOTE: symbology of the layer MUST be set first to unique values, if not it will result in some error like:
# AttributeError: 'Symbology' object has no attribute 'updateColorizer'

"""
for m in aprx.listMaps("historical"):
    for l in m.listLayers("Amon*"):
for m in aprx.listMaps("map"):
    for l in m.listLayers("Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_2091-2100_koppen_ko_FINAL*"):

"""

p = arcpy.mp.ArcGISProject("CURRENT")
for m in p.listMaps("map"):
    for l in m.listLayers("Amon_MRI-ESM2-0_historical_r5i1p1f1_gn_1971-2000_koppen_FINAL_CUBIC4*"):
        sym = l.symbology
        sym.updateColorizer('RasterUniqueValueColorizer')
        sym.colorizer.field = 'Value'
        for grp in sym.colorizer.groups:
            for item in grp.items:
                if item.label == '1':
                    item.label = "Af"
                    item.color = {'RGB': [150, 0, 0, 100]}
                elif item.label == '2':
                    item.label = "Am"
                    item.color = {'RGB': [255, 0, 0, 100]}
                elif item.label == '3':
                    item.label = "Aw"
                    item.color = {'RGB': [255, 204, 204, 100]}

                elif item.label == '4':
                    item.label = "BWh"
                    item.color = {'RGB': [255, 204, 0, 100]}
                elif item.label == '5':
                    item.label = "BWk"
                    item.color = {'RGB': [255, 255, 100, 100]}
                elif item.label == '6':
                    item.label = "BSh"
                    item.color = {'RGB': [204, 141, 20, 100]}
                elif item.label == '7':
                    item.label = "BSk"
                    item.color = {'RGB': [204, 170, 84, 100]}

                elif item.label == '8':
                    item.label = "Csa"
                    item.color = {'RGB': [0, 255, 0, 100]}
                elif item.label == '9':
                    item.label = "Csb"
                    item.color = {'RGB': [150, 255, 0, 100]}
                elif item.label == '10':
                    item.label = "Csc"
                    item.color = {'RGB': [200, 255, 0, 100]}
                elif item.label == '11':
                    item.label = "Cwa"
                    item.color = {'RGB': [180, 100, 0, 100]}
                elif item.label == '12':
                    item.label = "Cwb"
                    item.color = {'RGB': [150, 100, 0, 100]}
                elif item.label == '13':
                    item.label = "Cwc"
                    item.color = {'RGB': [90, 60, 0, 100]}
                elif item.label == '14':
                    item.label = "Cfa"
                    item.color = {'RGB': [0, 50, 0, 100]}
                elif item.label == '15':
                    item.label = "Cfb"
                    item.color = {'RGB': [0, 80, 0, 100]}
                elif item.label == '16':
                    item.label = "Cfc"
                    item.color = {'RGB': [0, 120, 0, 100]}

                elif item.label == '17':
                    item.label = "Dsa"
                    item.color = {'RGB': [255, 110, 255, 100]}
                elif item.label == '18':
                    item.label = "Dsb"
                    item.color = {'RGB': [255, 180, 255, 100]}
                elif item.label == '19':
                    item.label = "Dsc"
                    item.color = {'RGB': [230, 200, 255, 100]}
                elif item.label == '20':
                    item.label = "Dsd"
                    item.color = {'RGB': [200, 200, 200, 100]}
                elif item.label == '21':
                    item.label = "Dwa"
                    item.color = {'RGB': [200, 180, 255, 100]}
                elif item.label == '22':
                    item.label = "Dwb"
                    item.color = {'RGB': [154, 127, 179, 100]}
                elif item.label == '23':
                    item.label = "Dwc"
                    item.color = {'RGB': [135, 89, 179, 100]}
                elif item.label == '24':
                    item.label = "Dwd"
                    item.color = {'RGB': [111, 36, 179, 100]}
                elif item.label == '25':
                    item.label = "Dfa"
                    item.color = {'RGB': [50, 0, 50, 100]}
                elif item.label == '26':
                    item.label = "Dfb"
                    item.color = {'RGB': [100, 0, 100, 100]}
                elif item.label == '27':
                    item.label = "Dfc"
                    item.color = {'RGB': [200, 0, 200, 100]}
                elif item.label == '28':
                    item.label = "Dfd"
                    item.color = {'RGB': [200, 20, 133, 100]}
                elif item.label == '29':
                    item.label = "ET"
                    item.color = {'RGB': [100, 255, 255, 100]}
                elif item.label == '30':
                    item.label = "EF"
                    item.color = {'RGB': [100, 150, 255, 100]}
                elif item.label == '31':
                    item.label = "As"
                    item.color = {'RGB': [255, 153, 153, 100]}
                elif item.label == '0':
                    item.label = "Error"
                    item.color = {'RGB': [0, 0, 0, 100]}
l.symbology = sym
