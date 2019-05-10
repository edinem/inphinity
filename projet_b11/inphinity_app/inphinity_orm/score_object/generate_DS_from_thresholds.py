import csv
import time


class generateFromThresholds():

    binSize = 1

    def __init__(self, binSize):
        self.binSize = binSize

    def get_last_base_csv(self):
        filename = 'datasets/dataset_example.csv'
        file = open(filename, "r")

        return file;

    def generate_csv(self):
        filename = "datasets/" + time.strftime("%Y%m%d") + "_binsize_" + str(self.binSize) + ".csv"
        maxBin = 190
        filewriter = None
        csvfile = open(filename, "w+")
        nbColumns = (maxBin // int(self.binSize)) + 1
        header = ['Id_interactions']
        for i in range(0,nbColumns):
            header.append(',B' +str(i))

        filewriter = csv.DictWriter(csvfile, fieldnames=header,delimiter=",",extrasaction='ignore')
        filewriter.writeheader()


        with open('datasets/dataset_example.csv', "r") as f:
            reader = csv.reader(f)
            rowNr = 0
            arrayToWrite = []
            for row in reader:
                del arrayToWrite[:]
                if rowNr >= 1:
                    arrayToWrite = [row[0]]
                    lenRow = len(row) - 1
                    tmpTotal = 0
                    for i in range(1,lenRow):
                        if (i%int(self.binSize)) == 0:
                            arrayToWrite.append(","+str(tmpTotal))
                            tmpTotal = 0
                        tmpTotal = tmpTotal + int(row[i])

                    arrayToWrite.append("," + str(tmpTotal))
                    tmpArray = dict(zip(header,zip(*arrayToWrite)))
                    print(filewriter)
                    filewriter.writerow(tmpArray)
                rowNr = rowNr + 1

            csvfile.close()