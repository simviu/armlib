#include "arm/armZ1.h"

#ifdef WITH_ARM_Z1

using namespace arm;
using namespace unitree;

namespace{
   Posture conv(const Trans& T)
   {
      Posture p;
      p.pitch = toRad(T.e.p);
      p.roll = toRad(T.e.r);
      p.yaw = toRad(T.e.y);
      p.x = T.t.x();
      p.y = T.t.y();
      p.z = T.t.z();
      return p;
   }
   //----
   Trans conv(const Posture& p)
   {
       Trans T;
       T.t << p.x, p.y, p.z;
       T.e.y = p.yaw;
       T.e.r = p.roll;
       T.e.p = p.pitch;
       return T;
   }
}

//-----
bool ArmZ1::init()
{
    auto& uarm = *p_uarm_;
    log_i("Init Arm Z1...");
    uarm.sendRecvThread->start();
    //----
    log_i("Back to start...");
    uarm.backToStart();
    log_i("Now at start st.");

    sys::sleepMS(1000);
    log_i("Init Arm Z1 done");

    //--- init state
    uarm.setFsm(ArmFSMState::JOINTCTRL);
    uarm.labelRun("forward");

    //---- current st
    auto st = getSt();
    log_i("  Tip at: "+st.tip.str());
    return true;
}

//----- TODO: not yet
/*
bool ArmZ1::done()const
{
    auto& ctrlc = *pCtrlComp_;
    return ctrlc.recvState.state == ArmFSMState::JOINTCTRL;

}
*/

//-----
bool ArmZ1::moveTo(const TipSt& ts)
{
    auto& uarm = *p_uarm_;
    auto& cmd = uarm._trajCmd;
    auto& ctrlc = *pCtrlComp_;

    auto p = conv(ts.T);
    Vec6 v = PosturetoVec6(p);
    uarm.MoveJ(v,  ts.gripper, cfg_.maxSpeed);
    return true;

}
//-----
ArmSt ArmZ1::getSt()const
{
    ArmSt st;
    auto& rs = pCtrlComp_->recvState;
    st.tip.T = conv(rs.cartesianState);
    st.tip.gripper = rs.jointState[6].Pos;
    return st;
}


bool ArmZ1::test()
{
    auto& uarm = *p_uarm_;
    
    Vec6 posture[2];
    int order = 1;
    auto& ctrlc = *pCtrlComp_;

    uarm.labelRun("forward");
    auto& cmd = uarm._trajCmd;

    cmd.trajOrder = 0;//if order == 0, clear traj
    uarm.setTraj();

    // No.1 trajectory
    cmd.trajOrder = order++;
    cmd.trajType = TrajType::MoveJ;
    cmd.maxSpeed = 1.0;// angular velocity, rad/s
    cmd.gripperPos = 0.0;
    posture[0] << 0.5,0.1,0.1,0.5,-0.2,0.5;
    cmd.posture[0] = Vec6toPosture(posture[0]);
    uarm.setTraj();

    // No.2 trajectory
    cmd.trajOrder = order++;
    cmd.trajType = TrajType::Stop;
    cmd.stopTime = 1.0;
    cmd.gripperPos = -1.0;
    uarm.setTraj();


    // No.3 trajectory
    cmd.trajOrder = order++;
    cmd.trajType = TrajType::MoveL;
    cmd.maxSpeed = 0.3; // Cartesian velocity , m/s
    cmd.gripperPos = 0.0;
    posture[0] << 0,0,0,0.45,-0.2,0.2;
    cmd.posture[0] = Vec6toPosture(posture[0]);
    uarm.setTraj();

    // No.4 trajectory
    cmd.trajOrder = order++;
    cmd.trajType = TrajType::Stop;
    cmd.stopTime = 1.0; 
    cmd.gripperPos = -1.0;
    uarm.setTraj();

    // No.5 trajectory
    cmd.trajOrder = order++;
    cmd.trajType = TrajType::MoveC;
    cmd.maxSpeed = 0.3; // Cartesian velocity
    cmd.gripperPos = 0.0;
    posture[0] << 0,0,0,0.45,0,0.4;
    posture[1] << 0,0,0,0.45,0.2,0.2;
    cmd.posture[0] = Vec6toPosture(posture[0]);
    cmd.posture[1] = Vec6toPosture(posture[1]);
    uarm.setTraj();

    uarm.startTraj();
    // wait for trajectory completion
    while (ctrlc.recvState.state != ArmFSMState::JOINTCTRL){
        usleep(ctrlc.dt*1000000);
    }
    return true;
}

#endif // #ifdef WITH_ARM_Z1
