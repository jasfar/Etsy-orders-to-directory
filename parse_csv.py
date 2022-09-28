import re
import csv

import glob
import shutil
import os

input_filename = 'EtsySoldOrderItems2022-9-2.csv' # your Etsy csv goes here
output_filename = 'new_orders.csv'

cols_to_remove = ['Currency', 'Date-Paid', 'InPerson-Location', 'VAT-Paid-by-Buyer', 'Listings-Type', 'Transaction-ID', 'Item-Total', 'InPerson-Discount', 'SKU', 'Ship-City', 'Order-Type', 'Coupon-Code', 'Ship-Country', 'Shipping-Discount', 'Payment-Type', 'Price', 'Order-Sales-Tax', 'Order-ID', 'Buyer', 'Coupon-Details', 'Sale-Date', 'Discount-Amount', 'Ship-Name', 'Listing-ID', 'Ship-State', 'Ship-Address2', 'Order-Shipping', 'Ship-Zipcode', 'Date-Shipped', 'Ship-Address1', 'Quantity']

src_dir = "" # this is where the source files are, i.e. the files that will be cloned
dest_dir = "" # the destination folder

def copy_file_without_overwrite(src_name, dest_name, ext):

	# construct the src path and file name
	src_path_file_name = os.path.join(src_dir, src_name + ext)

	# construct the dest path and file name
	dest_path_file_name = os.path.join(dest_dir, dest_name + ext)

	# test if the destination file exists, if true, add parenthesese (i+1) to end of file, else, do the copy.
	i = 0
	while os.path.exists(dest_path_file_name):
		i += 1
		dest_path_file_name = dest_dir + '/' + dest_name + ' (' + str(i) + ')' + ext
	else:
		shutil.copyfile(src_path_file_name, dest_path_file_name)
		print("copy from %s to %s ok" % (src_path_file_name, dest_path_file_name))

# first, delete contents of destination directory, if there are any
for filename in os.listdir(dest_dir):
    file_path = os.path.join(dest_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

with open(input_filename, 'r') as csv_file:
	# clean up csv to not contain special characters like colons (:), replace spaces with dashes (-), remove wordy language, etc.
	csv_cleaned = (re.sub(r':|\s+', '-', line.strip()) for line in csv_file) 
	csv_cleaned = (re.sub(r'Color-|Variation-|-inches|-Peeker|-Sticker|-Decals|-Decal|\.|--', '', line.strip()) for line in csv_cleaned)
	csv_cleaned = (re.sub(r'(?!(([^"]*"){2})*[^"]*$),', "-", line.strip()) for line in csv_cleaned) # find commas inside double quotes ("") and replace with dash (-)

	csv_reader = csv.DictReader(csv_cleaned)

	# next(csv_reader) # skip the first line

	with open(output_filename, 'w') as new_file:
		fieldnames = ['Item-Name', 'Variations'] # columns to keep

		csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='_')

		# csv_writer.writeheader()

		for line in csv_reader:
			quantity = int(line['Quantity'])

			for col_index in cols_to_remove:
				del line[col_index]

			for q in range(quantity):
				csv_writer.writerow(line)

with open(output_filename, 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	for line in csv_reader:
		img_name = line[0]
		extension = '.png'
		copy_file_without_overwrite(img_name, img_name, extension)






