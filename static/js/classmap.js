var heatmapInstance;
function createHeatmap(pams, rows, columns, type) {// minimal heatmap instance configuration
  heatmapInstance = h337.create({
    // only container is required, the rest will be defaults
    container:  document.getElementById('heatmapContainer')
  });
  // now generate some random data
  var points = [];
  var max = 0;
  var width = 530;
  var height = 292.5;
  var len = pams.pam.length;

  for (i=0; i<len; ++i){
    var p = pams.pam[i];
    var val;
    if (type == "ar") {
      val = p.arousal;
      max = 4;
    } else if (type == "val"){
      val = p.valence;
      max = 4;
    } else if (type == "pa"){
      val = p.pa;
      max = 16;
    } else {
      val = p.na;
      max = 16;
    }

    var radius = 250;

    // if (max<val) {
    //   max = val;
    // }

    var xdist = (720-100*columns)/(columns+1);
    var ydist = (512-100*rows)/(rows+1);

    var jj = Math.floor(p.deskId/columns);
    var ii = p.deskId - jj*columns;
    
    var point = {
      x: (ii+0.5)*100+(ii+1)*xdist,
      y: (jj+0.5)*100+(jj+1)*ydist,
      value: val,
        // radius configuration on point basis
      radius: radius,
    };
    points.push(point);
  }
  
  // heatmap data format
  var data = { 
    max: max, 
    data: points 
  };
  // if you have a set of datapoints always use setData instead of addData
  // for data initialization
  heatmapInstance.setData(data);

}

function clearheatmap() {
  heatmapInstance.setData({data:[]});
}