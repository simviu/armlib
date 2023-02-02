#include "arm/armZ1.h"

#ifdef WITH_ARM_Z1

using namespace arm;
using namespace UNITREE_ARM;

namespace{
    struct LCfg{
        float grip_scl = -0.3; // 0 close, 1 open
    }; LCfg lc_;

    //----
    TipSt get_st_init()
    {
        TipSt st;
        st.T.t << 0.2, 0, 0.3;
        return st;
    }

    //----
    // TODO: remove conv(), use vec6 directly
   Posture conv(const Trans& T)
   {
      Posture p;
      p.rx = toRad(T.e.rx);
      p.ry = toRad(T.e.ry);
      p.rz = toRad(T.e.rz);
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
       T.e.rx = toDgr(p.rx);
       T.e.ry = toDgr(p.ry);
       T.e.rz = toDgr(p.rz);
       return T;
   }
}

//-----
bool ArmZ1::init()
{
    auto& uarm = *p_uarm_;
    log_i("Init Arm Z1(Connect to z1_ctrl_ROS/UDP)...");
    uarm.sendRecvThread->start();
    //----
//    log_i("Back to start...");
//    uarm.backToStart();
//    log_i("Now at start st.");

    sys::sleepMS(1000);
    log_i("Init Arm Z1 done");

    //--- init state
    uarm.setFsm(ArmFSMState::JOINTCTRL);
 // uarm.labelRun("forward");

    //---- move to init pos
    moveTo(get_st_init(), 1.0);

    //---- current st
    //auto st = getSt();
    //log_i("  Tip at: "+st.tip.str());
    return true;
}

//----- TODO: not yet

bool ArmZ1::done()const
{
    assert(p_uarm_!=nullptr);

    auto& cc = *p_uarm_->_ctrlComp;
    return cc.recvState.state == ArmFSMState::JOINTCTRL;

}


//-----
bool ArmZ1::moveTo(const TipSt& ts, float spd)
{
    assert(p_uarm_!=nullptr);
    auto& uarm = *p_uarm_;

    auto p = conv(ts.T);
    Vec6 v = PosturetoVec6(p);

    float spd1 = std::max(spd, cfg_.maxSpeed);
    float gr = ts.gripper * lc_.grip_scl;
    uarm.MoveJ(v,  gr, spd1);
    return true;

}
//-----
// Note : for z1 traj file, stored into :
//   ../config/Traj_<LABEL_NAME>.csv
bool ArmZ1::play(const string& sName)
{
    log_i("Arm play file:"+sName);

    assert(p_uarm_!=nullptr);
    auto& uarm = *p_uarm_;
    uarm.teachRepeat(sName);
    return true;
}

//-----
bool ArmZ1::getSt(ArmSt& st)
{
    assert(p_uarm_!=nullptr);
    auto& uarm = *p_uarm_;
    // TODO: validation
    auto& rs = uarm._ctrlComp->recvState;
    st.tip.T = conv(rs.cartesianState);
    st.tip.gripper = rs.jointState[6].Pos;
    st.joints.clear();
    for(int i=0;i<6;i++)
    {
        JointSt j; 
        j.r = rs.jointState[i].Pos;
        st.joints.push_back(j);
    }
    return true;
}


bool ArmZ1::test()
{
    log_e("ArmZ1::test() not yet");
    return false;
    /* // deprecated
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
    */
}

#endif // #ifdef WITH_ARM_Z1
