import os
import matplotlib.pyplot as plt

path = str()

path = input()
os.chdir(path)

folders = os.listdir(path)
print(folders)
for folder in folders:
    print(os.getcwd())
    print(folder)
    if os.path.isdir(folder):
        # if folder == ".DS_Store":
        #     continue
        files = os.listdir(folder)
        os.chdir(folder)
        print(os.getcwd())
        try:
            os.makedirs('../plots')
        except FileExistsError:
            pass

        for file in files:
            if file.endswith('.csv'):
                x = []
                y = []

                fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

                print(file)
                folder_name = os.path.basename(os.getcwd())
                # folder_name = folder
                graph_name = folder_name + '   ' + file

                ax1.set_title(graph_name)
                with open(file, 'r') as inp:
                    for line in inp:
                        line = line.split(',')
                        if line == ['\n']:
                            continue
                        else:
                            # print(line)
                            x.append(float(line[1]))
                            y.append(float(line[2].strip('\n')))
                    print(x)
                    print(y)
                    ax1.plot(x, y)
                    plt.axis('equal')
                    fig.savefig('../plots/' + graph_name + '.png')
        os.chdir('../')

# plt.show()


