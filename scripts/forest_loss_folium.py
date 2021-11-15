"""
This script is used to show data visualizations from
the poster "Google Earth Engine: Data and Information 
from the Cloud to your House" at the 9th International Fire Ecology 
and Management Congress

Execute it in the Google Earth Engine Code Editor and with the interactive map
select the Region of Interest (ROI) of your choice.

Authors: Isaac Arroyo-Velázquez , Enrique Camacho-Pérez
"""

# =============== L I B R A R I E S =============== #
import folium 
import ee
from branca.element import Template, MacroElement

# =============== F U N C T I O N S   &   M E T H O D S =============== #
def add_ee_layer(self, ee_image_object, vis_params, name):
    """Adds a method for displaying Earth Engine image tiles to folium map."""
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# =============== C O D E =============== #

ee.Initialize()

# Add Earth Engine drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Forest Cover Change
Img_Forest = ee.Image("UMD/hansen/global_forest_change_2020_v1_8")

# Select forest loss
Img_LossForest_Year = Img_Forest.select(['lossyear'])

# Region of Interest (ROI)
ROI = ee.Geometry.Rectangle([(-89.84, 21.18),(-88.09, 20.47)])

# Show forest loss over the years (ROI)
Img_LossForest_Year = Img_LossForest_Year.clip(ROI)

# Set visualization parameters
VisParams_LossForest_Year = {
  'min': 0, 
  'max': 20,
  'palette': ['001219', '005f73', '0a9396',
  '94d2bd', 'e9d8a6','ee9b00', 'ca6702',
  'bb3e03', 'ae2012', '9b2226']
}

map_forest_loss = folium.Map(location=[20.84,-89.01],zoom_start=9)
map_forest_loss.add_ee_layer(Img_LossForest_Year, VisParams_LossForest_Year, "Forest Loss (2000-2020)")

# Add a legend
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>
    Forest loss and
    <br>
    year of occurrence
    <br>
    (2001-2020)
</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:#001219;'></span>2001–2002 </li>
    <li><span style='background:#005f73;'></span>2003–2004 </li>
    <li><span style='background:#0a9396;'></span>2005–2006 </li>
    <li><span style='background:#94d2bd;'></span>2007–2008 </li>
    <li><span style='background:#e9d8a6;'></span>2009–2010 </li>
    <li><span style='background:#ee9b00;'></span>20011–2012 </li>
    <li><span style='background:#ca6702;'></span>20013–2014 </li>
    <li><span style='background:#bb3e03;'></span>20015–2016 </li>
    <li><span style='background:#ae2012;'></span>20017–2018 </li>
    <li><span style='background:#9b2226;'></span>20019–2020 </li>



  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

map_forest_loss.get_root().add_child(macro)

# Save the map
map_forest_loss.save('../maps/map_forest_loss_year_occurrence.html')
