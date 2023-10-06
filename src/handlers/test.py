import pandas as pd

data = {
    "city"  : ["New York", "Los Angeles", "Chicago", "San Francisco", "Miami", "Houston", "Seattle", "Boston", "Denver", "Austin", "Atlanta", "Phoenix", "Philadelphia", "Dallas", "San Diego", "Las Vegas", "Portland", "Nashville", "Detroit", "Minneapolis"],
    "street": ["Main Street", "Elm Street", "Oak Avenue", "Maple Drive", "Cedar Lane", "Pine Street", "Birch Road", "Willow Lane", "Sycamore Street", "Hickory Avenue", "Cypress Drive", "Magnolia Lane", "Poplar Avenue", "Juniper Road", "Spruce Lane", "Alder Street", "Redwood Avenue", "Aspen Lane", "Cherry Street", "Beech Road"],
    "number": [101, 202, 303, 404, 505, 606, 707, 808, 909, 111, 222, 333, 444, 555, 666, 777, 888, 999, 123, 456],
    "date"  : [2001, 2002, 2003, 1999, 1944, 2006, 1894, 2008, 2009, 2010, 1800, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
}

dataFrame = pd.DataFrame(data)
filterDate = dataFrame[dataFrame["date"] < 2006]

print(print(filterDate.to_string))