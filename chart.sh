echo file,geojson,pbf,pbfpacked;
for file in test/data/*.json;
    do echo $file,`./encode.py $file`,`./encode2.py $file`;
done
