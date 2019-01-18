# Generates directories to store barcoded specimen images
# can be used to create directories even if a specimen file
# doesn't exist yet to fill it.
prefix='BRIT'
start=0
end=150000
inc=10000
x=$start
digits=${#end}+1
while [ $x -le $end ]
do
  # pad all directories names with 0 to have the same number of characters
  # this approach is NOT used in the current version of sort.py
  #dirname=`printf "$prefix%.$((((l=$digits-${#x})>0)*l))d%s\n" 0 "$x"`
  # name directories with prefix and number, no padding
  dirname=`printf "$prefix%s\n" "$x"`
  echo Making $dirname
  mkdir -p $dirname
  x=$(( $x + $inc ))
done
