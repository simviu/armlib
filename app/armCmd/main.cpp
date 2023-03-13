/*
   Author: Sherman Chen
   Create Time: 2022-12-04
   Email: schen@simviu.com
   Copyright(c): Simviu Inc.
   Website: https://www.simviu.com
 */

#include "arm/armLib.h"
#include "arm/armZ1.h"

using namespace arm;
using namespace ut;

namespace{
  //---------
  // register_arms
  //---------

  void register_arms()
  {

#ifdef WITH_ARM_Z1
      Arm::addCreator("z1",[]()->Sp<Arm>{
        return mkSp<UNITREE_ARM::ArmZ1>();
      });        
#endif 

  }
}
//----------
// main
//----------
int main(int argc, char ** argv)
{
    register_arms();
    ArmMng ac;
    return ac.run(argc, argv);
}
