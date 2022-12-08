#include "arm/armTest.h"

using namespace test; 
namespace{
    void wait_done(const Arm& arm)
    {
        
     // while(!arm.done())
        for(int i=0;i<20;i++)
        {
            sys::sleepMS(100);
            auto st = arm.getSt();
            log_i("Tip : " + st.tip.str());
        }
    }
}
//----
bool ArmTest::test_basic()const
{
    auto p_arm = Arm::create("z1");
    assert(p_arm!=nullptr);
    auto& arm = *p_arm;
    arm.init();
    arm.test();    
    return true;
}

//----------
bool ArmTest::test_moveTo()const
{
    auto p_arm = Arm::create("z1");
    assert(p_arm!=nullptr);
    auto& arm = *p_arm;

    arm.init();


    TipSt ts;

    //-----1
    log_i("-------------- Pose 1");
    ts.gripper = 0;
    ts.T.t << 0.2, -0.18, 0.3;
    ts.gripper = 0.3;
    ts.T.e = Euler(0, 45,0);

//    ts.T.t <<  0,0.3,0.4;
 //   ts.T.e = Euler(M_PI/2,0,0);

    log_i("arm moveTo: "+ts.T.str()+"...");
    arm.moveTo(ts);
    wait_done(arm);
    log_i("arm moveTo done. ");
    sys::sleepMS(2000);

    //----2
    log_i("-------------- Pose 2 ");
    
    ts.gripper = -0.3;
    ts.T.t << -0.3,-0.1,0.4;
    ts.T.e = Euler(180,0,0);
    log_i("arm moveTo: "+ts.T.str()+"...");
    arm.moveTo(ts);
    wait_done(arm);
    log_i("arm moveTo done. ");
    
    //----3
    log_i("-------------- Pose 2 ");
    
    ts.gripper = 0;
    ts.T.e = Euler(180*0.9,0,0);
    log_i("arm moveTo: "+ts.T.str()+"...");
    arm.moveTo(ts);
    wait_done(arm);
    log_i("arm moveTo done. ");
    

    //----
    sys::sleepMS(3000);
    return true;
}


//----------
// run
//----------
bool ArmTest::run()
{
    log_i("Arm test running...");
 //   test_basic();
    test_moveTo();
    return true;
}
