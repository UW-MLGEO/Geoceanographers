
while read url; do
  wget -r -np -nH --cut-dirs=6 -A "*.csv" "$url"
done < webservers.txt

