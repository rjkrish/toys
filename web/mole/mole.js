var board = 
[ 
 [{"shape": "square"},{"shape": "square"}, {"shape": "square"}],
 [{"shape": "square"},{"shape": "square"}, {"shape": "square"}],
 [{"shape": "square"},{"shape": "square"}, {"shape": "square"}],
 [{"shape": "square"},{"shape": "square"}, {"shape": "square"}]
]

/*-------------------------------------------
TODO: 
1. Randomize color
2. Make grid responsive
-------------------------------------------*/

var boardRows = board.length;
// assume equal number of columns in each row
var boardCols = board[0].length;

var currRow = 0;
var currCol = 0;

var clicks = 0;

var run = true;

function fill (cel, color) {
  cel.css('background-color', color);
}

function cell(r, c){
	return $('#c' + r + '' + c);
}

function checkClick(e) {
  clicks++;

  if ( e.target.id == 'c' + currRow + '' + currCol ){
       alert('Whack!! ' + clicks + ' tries.' );
       clicks = 0;
  }
  e.stopPropagation();
}

/**
  Return a random number between 0 and max excluding max.
*/
function randBelow(max){
	return Math.floor(Math.random() * max);
}

function drawBoard() {
  var r = 0;
  var c = 0;	
  var b = $('#board');
  var heightPct = Math.ceil(80 / boardRows) + '%';
  var widthPct = Math.ceil(80 / boardCols) + '%';

  //console.log('w,h', widthPct, heightPct);

  for (r = 0; r < boardRows; r++){
  	for(c = 0; c < boardCols; c++){
  	  var s = board[r][c].shape;
      b.append( '<div id="c' + r + '' + c + '" class="' + s + '"></div>'); 
      cell(r,c).click(checkClick);
      //cell(r,c).css('height', heightPct);
      //cell(r,c).css('width', widthPct);     
    }  
  }
}

 
function play() {

  var prevRow = currRow;
  var prevCol = currCol;

  currRow = randBelow(boardRows);
  currCol = randBelow(boardCols);
  
  fill(cell(prevRow, prevCol), '#000000');
  fill(cell(currRow, currCol), '#3333EE');
  
  setTimeout(play, 500);
}

drawBoard();

play();