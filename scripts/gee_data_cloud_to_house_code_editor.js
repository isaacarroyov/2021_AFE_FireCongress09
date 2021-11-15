/*
This script is used to show data visualizations from
the poster "Google Earth Engine: Data and Information 
from the Cloud to your House" at the 9th International Fire Ecology 
and Management Congress

Execute it in the Google Earth Engine Code Editor and with the interactive map
select the Region of Interest (ROI) of your choice.

Authors: Isaac Arroyo-Velázquez , Enrique Camacho-Pérez
*/

/* GET THE DATA */
// Temperature 
var ImgColl_Temperature = ee.ImageCollection("MODIS/006/MOD11A1");
// Precipitation
var ImgColl_Precipitation = ee.ImageCollection("UCSB-CHG/CHIRPS/PENTAD");
// Forest Cover Change
var Img_Forest = ee.Image("UMD/hansen/global_forest_change_2020_v1_8");

/*
FILTER BY DATE
This filter is only applied to Image Collections
*/

// 5 Years, from Jan 2016 to Dec 2020
var Date_Start = '2016-01-01';
var Date_End = '2020-12-31';

// Apply filters to data
var ImgColl_Temperature = ImgColl_Temperature.filterDate(Date_Start, Date_End);
var ImgColl_Precipitation = ImgColl_Precipitation.filterDate(Date_Start, Date_End);

/* SELEC BANDS */
var ImgColl_Temperature = ImgColl_Temperature.select(['LST_Day_1km']);
var ImgColl_Precipitation = ImgColl_Precipitation.select(['precipitation']);
var Img_LossForest_Year = Img_Forest.select(['lossyear']);

/* UNIT CONVERSION (TEMPERATURE) */

var func_kelvin_to_celsius = function(image){
  var scale_image = image.multiply(0.02);
  var to_celsius = scale_image.subtract(273.15);
  var final = to_celsius.copyProperties(image, ['system:time_start']);
  return final;
  };

var ImgColl_Temperature = ImgColl_Temperature.map(func_kelvin_to_celsius);

/* DATA VISUALIZATION */

/* Time series */
var Plot_Temp = ui.Chart.image.series(
  {
    // Image collection
    imageCollection: ImgColl_Temperature,
    // Region of Interest (Geometry)
    region: ROI,
    // Reducer (statistic, usually)
    reducer: ee.Reducer.mean(),
    // Scale 
    scale: 1000,
    // X-axis property
    xProperty: 'system:time_start'
  }
);
print("Time series – Temperature (2016-202)");
print(Plot_Temp);

var Plot_Prec = ui.Chart.image.series(
  ImgColl_Precipitation,
  ROI,
  ee.Reducer.mean(),
  1000,
  'system:time_start'
  );

print("Time series – Precipitation (mm/5day)");
print(Plot_Prec);



// Set visualization parameters
var VisParams_Temperature = {
  min: 27,
  max: 34,
  palette:['blue', 'limegreen', 'yellow', 'darkorange', 'red']
};

var VisParams_Precipitation = {
  min: 15,
  max: 30,
  palette: ['00B4D8','0096C7','0077B6','023E8A','03045E']
};
var VisParams_LossForest_Year = {
  min: 0, 
  max: 20,
  palette: ['001219', '005f73', '0a9396',
  '94d2bd', 'e9d8a6','ee9b00', 'ca6702',
  'bb3e03', 'ae2012', '9b2226']
};

// Information displayed
// Show mean temperature and precipitation
var Img_Temperature = ImgColl_Temperature.mean()
                  .clip(ROI); //display only the region of interest
var Img_Precipitation = ImgColl_Precipitation.mean().clip(ROI);
// Show forest loss over the years
var Img_LossForest_Year = Img_LossForest_Year.clip(ROI);

// Add layers of information
Map.centerObject(ROI); //Center map
Map.addLayer(Img_Temperature,VisParams_Temperature, 'Mean Temperature (2016-2020)');
Map.addLayer(Img_Precipitation,VisParams_Precipitation, 'Mean Precipitation (2016-2020)');
Map.addLayer(Img_LossForest_Year,VisParams_LossForest_Year, 'Forest Loss (2000-2020)');

