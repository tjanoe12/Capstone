import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from bins import scanDict, bins, missing_values_dict

invalid_input = True


def start():
    print('Mass Spectrometry Viewer V 1.0\nTaylor Janoe Student ID: 00718244')
    start = input("Type 'start' to begin: ")
    if start == 'start':
        # filePath = input("Enter the file path for the scan data")
        showData = input("Type scan to see a selected scan's M/Z and Intensity\n"
                         "Type bins to see a selected bin's deviation across all scans processed\n"
                         "Type examine to view how to data varies across all scans in accuracy\n: ")

        while showData == str('scan'):
            if showData == 'scan':
                try:
                    print('To return to the main menu type main')
                    scan_lookup = input('Enter a scan to view the M/z and Intensity plot, ie. Scan1.csv or Scan2.csv: ')
                    if scan_lookup == 'main':
                        break
                    mass = scanDict[scan_lookup]['M/Z']
                    intensity = scanDict[scan_lookup]['Intensity']
                    sns.scatterplot(x=mass, y=intensity)
                    plt.show()
                except KeyError:
                    print("Invalid file name, try again.")
                    continue

        while showData == str('bins'):
            print('To return to the main menu type main')
            view_bins_keys = input('If you would like to see a list of mass bins enter yes, if not, no: ')
            if view_bins_keys == 'yes':
                print(list(bins.keys()))
            elif view_bins_keys == 'main':
                break
            else:
                None
            bin_lookup = float(input('Enter a mass to view the bin data: '))
            try:
                print(bins[bin_lookup])
                mass = bins[bin_lookup]['masses']
                leftEdge = -(bin_lookup - bins[bin_lookup]['leftEdge'])
                rightEdge = bins[bin_lookup]['rightEdge'] - bin_lookup
                deviationList = []
                for m in mass:
                    deviation = m - bin_lookup
                    deviationList.append(deviation)
                d = {'mass': mass, 'deviation': deviationList}
                d = pd.DataFrame(d)
                graph = sns.regplot(x="mass", y="deviation", data=d)
                graph.axhline(y=rightEdge, color='g')
                graph.axhline(y=leftEdge, color='g')
                plt.title(bin_lookup)
                plt.show()
                remove_scans = input("To remove scans from the bin view type remove\n"
                                     "To adjust ppm window type adjust\n"
                                     "To go to the main menu type main: ")
                while remove_scans == 'remove':
                    try:
                        print('To return to the main menu type main')
                        scans_to_remove = input("enter the scan file name to remove it from the bin: ")
                        if scans_to_remove == 'main':
                            break
                        scan_removed_index = bins[bin_lookup]['scans'].index(scans_to_remove)
                        removing_from_scan = bins[bin_lookup]['scans'].pop(scan_removed_index)
                        mass_index = bins[bin_lookup]['masses'].pop(scan_removed_index)
                        mass = bins[bin_lookup]['masses']
                        leftEdge = -(bin_lookup - bins[bin_lookup]['leftEdge'])
                        rightEdge = bins[bin_lookup]['rightEdge'] - bin_lookup
                        deviationList = []
                        for m in mass:
                            deviation = m - bin_lookup
                            deviationList.append(deviation)
                        d = {'mass': mass, 'deviation': deviationList}
                        d = pd.DataFrame(d)
                        graph = sns.regplot(x="mass", y="deviation", data=d)
                        for i in range(d.shape[0]):
                            plt.text(x=d.mass[i] + 0.3, y=d.deviation[i] + 0.3, s=d.mass[i],
                                     fontdict=dict(color='green', size=10),
                                     bbox=dict(facecolor='blue', alpha=0.5))
                        graph.axhline(y=rightEdge, color='g')
                        graph.axhline(y=leftEdge, color='g')
                        plt.title(bin_lookup)
                        plt.show()
                    except ValueError:
                        print("Scan name is not in the system, please try again.")
                        continue

                    replace_scans = input("Would you like to keep the scan and masses in the bin? Type yes or no: ")
                    try:
                        if replace_scans == 'yes':
                            bins[bin_lookup]['masses'].append(mass_index)
                            bins[bin_lookup]['scans'].append(scans_to_remove)
                            mass = bins[bin_lookup]['masses']
                            leftEdge = -(bin_lookup - bins[bin_lookup]['leftEdge'])
                            rightEdge = bins[bin_lookup]['rightEdge'] - bin_lookup
                            deviationList = []
                            for m in mass:
                                deviation = m - bin_lookup
                                deviationList.append(deviation)
                            d = {'mass': mass, 'deviation': deviationList}
                            d = pd.DataFrame(d)
                            graph = sns.regplot(x="mass", y="deviation", data=d)
                            graph.axhline(y=rightEdge, color='g')
                            graph.axhline(y=leftEdge, color='g')
                            plt.title(bin_lookup)
                            plt.show()

                        else:
                            break

                    except ValueError:
                        print("Invalid scan name try again")
                        continue
                while remove_scans == 'adjust':
                    adjust_ppm_number = int(input(
                        "To adjust the ppm window please enter a number 1-9. All Deviations are set to 10ppm on either side of the mass: "))
                    if adjust_ppm_number in range(1, 10):
                        newEdges = (adjust_ppm_number / 1000000) * bin_lookup
                        mass = bins[bin_lookup]['masses']
                        leftEdge = -newEdges
                        rightEdge = newEdges
                        deviationList = []
                        for m in mass:
                            deviation = m - bin_lookup
                            deviationList.append(deviation)
                        d = {'mass': mass, 'deviation': deviationList}
                        d = pd.DataFrame(d)
                        graph = sns.regplot(x="mass", y="deviation", data=d)
                        graph.axhline(y=rightEdge, color='g')
                        graph.axhline(y=leftEdge, color='g')
                        plt.title(bin_lookup)
                        plt.show()
                        break
                    else:
                        print("Invalid entry please enter a number between 1 and 9: ")
                if remove_scans == 'main':
                    break
                else:
                    break
            except KeyError:
                print("Invalid bin try again")
                break
            except ValueError:
                start()
                print("Invalid bin try again")

        while showData == 'examine':
            print('To view the main menu type main')
            describe = input('To view descriptive statistical data type stats, to view missing data type missing: ')
            if describe == 'stats':
                print('The number of Scans is: ' + str(len(scanDict)))
                print('The number of Bins is: ' + str(len(bins)))
                s = []
                for key in bins:
                    a = (bins[key]['mean'])
                    s.append(float(bins[key]['standardDeviation']))
                    try:
                        if a != None:
                            print('Bins with descriptive data: ', key, bins[key])
                    except TypeError:
                        next(key)
                average_standard_deviation = (sum(s) / len(s))
                print('The average standard deviation across bins is: ', average_standard_deviation)
                continue
            elif describe == 'missing':
                view_missing = input('To view a list of scans with missing elements type yes or type no to continue to enter a scan view of missing elemenmts: ')
                if view_missing == 'yes':
                    print(missing_values_dict.keys())
                else:
                    None
                missing_scans_lookup = input('Type the name of the scan to see its missing data information: ')
                try:
                    print(missing_values_dict[missing_scans_lookup])
                except KeyError:
                    print('Invalid entry please try again')
                    continue
                except ValueError:
                    print('Invalid entry please try again')
                    continue
            elif describe == 'main':
                break

    elif start == 'exit':
        exit()


while invalid_input:
    try:
        start()
    except ValueError:
        start()
    except TypeError:
        start()
