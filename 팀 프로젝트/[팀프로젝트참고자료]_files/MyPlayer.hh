
//////////////////////////////////////////////////////////////
//
// File: MyPlayer.hh
// Name: Sanguk Noh
// Description: Reflex Agent With State
// 
//////////////////////////////////////////////////////////////

#ifndef __MyPlayer_HH__
#define __MyPlayer_HH__

typedef enum { CHEATER, STUPID, RANDOM, HUMAN, INTELLIGENT } Mode;

// There are possible states in the simple reflex environment. 
typedef enum { UNKNOWN, SAFE, WALLS, BUMPS, GOALS, GOLDS, BREEZES, PITS, STENCHES, WUMPI } WhatWorld; 

// To maintain my direction.
typedef enum { E, W, N, S } Direction;

//
// This is the definition of your Player class.  It is a subclass
// of class "Player".
//
// The 6 method you may have are:
//
// A constructor
// A destructor
//
// void configure ( const char * )            - Command Line Arguments for Player
// void reset()                               - Resets the Player at the beginning of
//                                              each trial.
// const Action process ( const Percept & )   - Takes a percept and returns an action.
//                                              (This is the only required method.)
// void done()                                - Called with Game is over.
//

#include "Player.hh"
#include "WumpusEnvironment.hh"

//
// This is a State class.
//
class State
{
public:
  State();
  ~State();
  void SetWalls(int x, int y) { Grid[GridSize*x + y] = WALLS; }
  void SetBumps(int x, int y) { Grid[GridSize*x + y] = BUMPS; }
  void SetGoals(int x, int y) { Grid[GridSize*x + y] = GOALS; }
  void SetGolds(int x, int y) { Grid[GridSize*x + y] = GOLDS; }
  void SetBreezes(int x, int y) { Grid[GridSize*x + y] = BREEZES; }
  void SetPits(int x, int y) { Grid[GridSize*x + y] = PITS; }
  void SetStenches(int x, int y) { Grid[GridSize*x + y] = STENCHES; }
  void SetWumpi(int x, int y) { Grid[GridSize*x + y] = WUMPI; }
  void SetSafe(int x, int y) { Grid[GridSize*x + y] = SAFE; }
  WhatWorld GetState(int x, int y) { return Grid[GridSize*x + y]; }

  void SetMyPos(int x, int y) { MyPos_x = x; MyPos_y = y; }
  int GetMyPosX() { return MyPos_x; }
  int GetMyPosY() { return MyPos_y; }
  Direction GetDirection() { return MyHeading; }
  void SetDirection(Direction d) { MyHeading = d; }
  static int MyPos_x, MyPos_y;
  static Direction MyHeading;

protected:
  const int GridSize = 12; // maximum grid size + 2
  WhatWorld *Grid;
};

int State::MyPos_x = 1;
int State::MyPos_y = 1;
Direction State::MyHeading = E;

class MyPlayer : public Player
{
public:
  MyPlayer();
  virtual ~MyPlayer();

  virtual void configure ( const char *arg );
  virtual void reset();
  virtual const Action process ( const Percept &percept );
  virtual void done();

protected:
// Functions for each intelligent agent.
  State cur_state;
  void UpdateState ( const Percept &percept );
  const Action ChooseAction ();

  Mode mode;
};

#endif




