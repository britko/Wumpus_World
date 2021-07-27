
//////////////////////////////////////////////////////////////
//
// File: MyPlayer.cc
// Name: Sanguk Noh
// Description: Reflex Agent With State
// 
//////////////////////////////////////////////////////////////

#include "MyPlayer.hh"
#include "RndGen.hh"
#include "GridEnvironment.hh"
#include <iostream.h>
#include <iomanip.h>

//
// Global static variable of your player's class
//
static MyPlayer player;

//
// Your Player's class constructor
//
MyPlayer::MyPlayer()
{
  mode = INTELLIGENT;       // default mode: Each homework
}

//
// Your Player's class destructor
//
MyPlayer::~MyPlayer()
{
}

//
// Your Player's optional configuration method
//
// This method will be called if a "-p" option
// is given on the command line.
//
void MyPlayer::configure( const char *a )
{
  String arg ( a );
  Regex cheat  ( "c\\(heat\\(er\\)?\\)?" );
  Regex random ( "r\\(and\\(om\\)?\\)?" );
  Regex stupid ( "s\\(tupid\\|uicid\\(e\\|al\\)\\)?" );
  Regex simple ( "si\\(mple\\)?" );
  
  if ( arg.matches ( cheat ) )
    mode = CHEATER;

  if ( arg.matches ( random ) )
    mode = RANDOM;

  if ( arg.matches ( stupid ) )
    mode = STUPID;

  if ( arg.matches ( simple ) )
    mode = INTELLIGENT;

  switch ( mode )
    {
    case CHEATER: cout << "MyPlayer Cheats." << endl; break;
    case STUPID:  cout << "MyPlayer is Suicidal." << endl; break;
    case RANDOM:  cout << "MyPlayer is Random." << endl; break;
    case INTELLIGENT:  cout << "MyPlayer is Intelligent." << endl; break;
    case HUMAN:   cout << "MyPlayer is a Human." << endl; break;
    }
}

//
// Your Player's reset method
// Reset the initial position and heading.
//
void MyPlayer::reset()
{
  State::MyPos_x = 1;
  State::MyPos_y = 1;
  State::MyHeading = E;
}

//
// Your Player's process method
//
// This is the method that will be called with each percept.
// The Player superclass provides you with lists of all previous
// percepts you have seen and all previous actions you have taken.
// When this method is invoked, the percept passed in already will
// have been added to the Percept List.
//
// See the Simulation Handout for instructions on accessing the
// Percept and Action lists.
//

static Action cheatActions[] = { TURN_LEFT, SHOOT, GOFORWARD, GOFORWARD, TURN_RIGHT, GOFORWARD, GRAB, TURN_RIGHT, GOFORWARD, GOFORWARD, TURN_RIGHT, GOFORWARD, CLIMB };
static Action stupidActions[] = { TURN_LEFT, SHOOT, GOFORWARD, GOFORWARD, TURN_RIGHT, GOFORWARD, GRAB, GOFORWARD };

const Action MyPlayer::process ( const Percept &percept )
{
  cout << "Percept: " << percept << endl;
#ifdef EXTENDED_PERCEPT
  cout << percept.getImage() << endl;
#endif

  switch ( mode )
    {
    case CHEATER:
      return cheatActions[ actionList.length() ];
      
    case STUPID:
      return stupidActions[ actionList.length() ];
      
    case RANDOM:
      return ( Action ) ( randInt ( CLIMB ) );

    case INTELLIGENT:
      this.UpdateState( percept );
      return ChooseAction ();

    case HUMAN:
      break;
    }

  Action action;
  char c;
  
  cout << "Action (l,r,f,g,s,c): ";
  cin >> c;

  switch ( c )
    {
    case 'l': action = TURN_LEFT;  break;
    case 'r': action = TURN_RIGHT; break;
    case 'f': action = GOFORWARD;  break;
    case 'g': action = GRAB;       break;
    case 's': action = SHOOT;      break;
    case 'c': action = CLIMB;      break;
    }

  return action;
}

//
// This method is called after a game has ended, either by the player
// climbing out of the cave, dying, or the maximum number of steps has
// been reached.
//
void MyPlayer::done()
{
  int x, y;

  x=cur_state.GetMyPosX();
  y=cur_state.GetMyPosY();

  cout << "current location x: " << x;
  cout << " current location y: " << y << "\n";

  // Set the location of Pit and Wumpus.
  if ( perceptList[LL::last].isBreeze() ) cur_state.SetPits(x,y);
  if ( perceptList[LL::last].isStench() ) cur_state.SetWumpi(x,y);
}


////////////////////////////////////////////////////////////////////////
//
// Reflex Agent with State.
//
////////////////////////////////////////////////////////////////////////


// State Constructor
// At first, the status of grid world (nxn) is UNKNOWN.
State::State() 
{
  Grid = new WhatWorld [GridSize*GridSize];

  for (int i=0; i<GridSize; i++)
    for (int j=0; j<GridSize; j++)
      Grid[GridSize*i + j] = UNKNOWN;

  // 0..11 : X Walls
  for (int i=0; i<GridSize; i++)
    Grid[i] = WALLS;

  // 0, 12, 24, ... : Y Walls
  for (int i=0; i<GridSize; i++)
    Grid[GridSize*i + 0] = WALLS;

  // Initial state should be SAFE and Direction is EAST.
  Grid[GridSize+1] = SAFE;
  MyHeading = E;
 
  // Set the initial position and the action sequence.
  this.SetMyPos(1,1);
}

// State Destructor
State::~State() 
{
  delete [] Grid;
}


//
// This procedure changes the State based on the recently received percept.
//
void MyPlayer::UpdateState ( const Percept &percept ) 
{
  int x, y;

  x=cur_state.GetMyPosX();
  y=cur_state.GetMyPosY();

  cout << "current location x: " << x;
  cout << " current location y: " << y << "\n";

  if ( (numGold()>0) && (x==1) && (y==1) ) cur_state.SetGoals(x,y);
  else if ( (percept.isGlitter()) && (numGold()==0) ) cur_state.SetGolds(x,y); 
  else if ( percept.isBump() ) {
    cur_state.SetBumps(x,y);
    switch ( cur_state.GetDirection() ) {
    case E: cur_state.SetWalls(x+1,y); break;
    case W: cur_state.SetWalls(x-1,y); break;
    case N: cur_state.SetWalls(x,y+1); break;
    case S: cur_state.SetWalls(x,y-1); break;
    }
  }
  else if ( percept.isStench() ) cur_state.SetStenches(x,y);
  else if ( percept.isBreeze() ) cur_state.SetBreezes(x,y);
  else cur_state.SetSafe(x,y);
}


//
// Choose Action Procedure.
//
const Action MyPlayer::ChooseAction () 
{
  Action action;
  int x, y;

  x = cur_state.GetMyPosX();
  y = cur_state.GetMyPosY();

  if (actionList.length() > 0) cout << "Action List: " << actionList[LL::last] << "\n";

  switch ( cur_state.GetState(x,y) ) {
  case GOALS: action = CLIMB; break;
  case GOLDS: action = GRAB; break;
  case BREEZES:
    switch ( cur_state.GetDirection() ) {
    case E: 
      if ( cur_state.GetState(x+1,y)==PITS ) {
	action = TURN_LEFT;
	cur_state.SetDirection(N); 
      }
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x+1,y); 
      }
      break;
    case W: 
      if ( cur_state.GetState(x-1,y)==PITS ) {
	action = TURN_LEFT;
	cur_state.SetDirection(S); 
      }
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x-1,y); 
      }
      break;
    case N: 
      if ( cur_state.GetState(x,y+1)==PITS ) {
	action = TURN_LEFT;
	cur_state.SetDirection(W); 
      }
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x,y+1); 
      }
      break;
    case S: 
      if ( cur_state.GetState(x,y-1)==PITS ) {
	action = TURN_LEFT;
	cur_state.SetDirection(E); 
      }
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x,y-1); 
      }
      break;
    }
    break;
  case STENCHES:
    switch ( cur_state.GetDirection() ) {
    case E: 
      if ( (cur_state.GetState(x+1,y)==WUMPI) && (numArrows()>0) ) action = SHOOT;
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x+1,y); 
      }
      break;
    case W: 
      if ( (cur_state.GetState(x-1,y)==WUMPI) && (numArrows()>0) ) action = SHOOT;
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x-1,y); 
      }
      break;
    case N: 
      if ( (cur_state.GetState(x,y+1)==WUMPI) && (numArrows()>0) ) action = SHOOT;
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x,y+1); 
      }
      break;
    case S: 
      if ( (cur_state.GetState(x,y-1)==WUMPI) && (numArrows()>0) ) action = SHOOT;
      else {
	action = GOFORWARD;
	cur_state.SetMyPos(x,y-1); 
      }
      break;
    }
    break;
  case BUMPS: 
    if ( (actionList[LL::last] == TURN_LEFT) || (actionList[LL::last] == TURN_RIGHT) ) { 
      action = GOFORWARD;
      switch ( cur_state.GetDirection() ) {
      case E: cur_state.SetMyPos(x+1,y); break;
      case W: cur_state.SetMyPos(x-1,y); break;
      case N: cur_state.SetMyPos(x,y+1); break;
      case S: cur_state.SetMyPos(x,y-1); break;
      }
    }
    else {
      switch ( cur_state.GetDirection() ) {
      case E:
	if ( cur_state.GetState(x-1,y-1) == WALLS ) {
	  action = TURN_LEFT;
	  cur_state.SetDirection(N);
	} 
	else {
	  action = TURN_RIGHT;
	  cur_state.SetDirection(S);
	} 
	cur_state.SetMyPos(x-1,y);
	break;
      case W: 
	if ( cur_state.GetState(x+1,y-1) == WALLS ) {
	  action = TURN_RIGHT;
	  cur_state.SetDirection(N);
	} 
	else {
	  action = TURN_LEFT;
	  cur_state.SetDirection(S);
	} 
	cur_state.SetMyPos(x+1,y);
	break;
      case N: 
	if ( cur_state.GetState(x-1,y-1) == WALLS ) {
	  action = TURN_RIGHT;
	  cur_state.SetDirection(E);
	} 
	else {
	  action = TURN_LEFT;
	  cur_state.SetDirection(W);
	} 
	cur_state.SetMyPos(x,y-1);
	break;
      case S: 
	if ( cur_state.GetState(x-1,y+1) == WALLS ) {
	  action = TURN_LEFT;
	  cur_state.SetDirection(E);
	} 
	else {
	  action = TURN_RIGHT;
	  cur_state.SetDirection(W);
	} 
	cur_state.SetMyPos(x,y+1);
	break;
      }
    }
    break;
  default:         
    action = GOFORWARD;
    switch ( cur_state.GetDirection() ) {
    case E: cur_state.SetMyPos(x+1,y); break;
    case W: cur_state.SetMyPos(x-1,y); break;
    case N: cur_state.SetMyPos(x,y+1); break;
    case S: cur_state.SetMyPos(x,y-1); break;
    }
    break;
  }

  return action;
}









