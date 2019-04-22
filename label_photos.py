import os

with open('labels.txt') as f:
    labels = f.readlines()
labels = [x.strip().replace('\n','').replace(' ','').replace('\t','') 
                    for x in labels]

print(f'Found {len(labels)} labels.')

filename_labels = []
label_counts = {}
for label in labels:
    new_label = label
    if label in label_counts.keys():
        label_counts[label] = label_counts[label]+1
        new_label = f'{new_label}_{label_counts[label]}'
    else:
        label_counts[label] = 1

    filename_labels.append(new_label)


print(f'Made the {len(filename_labels)} labels unique.')

path_to_photos = 'photos'
directory_list = os.listdir(path_to_photos).sort()
for i,fname in enumerate(directory_list):
    print(fname)
    ext = fname.split('.')[-1]
    src = f'{path_to_photos}/{fname}'
    dest = f'{path_to_photos}/{filename_labels[i]}.{ext}'
    os.rename(src, dest) 