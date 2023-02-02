#include "arm/armLib.h"
#include "arm/armZ1.h"
#include "arm/armTcp.h"

using namespace arm;

//------
string Trans::str()const
{ 
    return "{t:\""+vsn::str(t,3)+
            "\", euler:\"" +e.str()+"\"}";  
}

//-----
bool Trans::set(const string& s)
{
    vector<double> ds;
    if(!s2data(s, ds, ',')) 
        return false;
    if(ds.size()<6) 
        return false;

    t << ds[0], ds[1], ds[2];
    e.rx = ds[3];
    e.ry = ds[4];
    e.rz = ds[5];
    return true;
}

//----
string ArmSt::str()const
{
    string sj;
    int N = joints.size();
    for(int i=0;i<N;i++)
        sj += ((i==0)?"":",")+::str(joints[i].r);
    string s = "{ tip:"+tip.str() + 
               ", joints:["+sj+"] }";
    return s;
        
}
//---- factory
Sp<Arm> Arm::create(const string& sModel)
{
    //--- check if remote
    size_t nf = sModel.find("robot://");
    if(nf!=string::npos)
    {
        string sUri = sModel.substr(nf+8);
        return mkSp<ArmTcp>(sUri);
    }
    else if(sModel=="dummy")
        return mkSp<Arm>();

#ifdef WITH_ARM_Z1
    else if(sModel=="z1")
        return mkSp<UNITREE_ARM::ArmZ1>();
#endif 

    log_e("Unkonw Arm type:'"+sModel+"'");
    return nullptr;

}
//----
void Arm::waitDone()
{
    while(!done())
        sys::sleep(0.01);
}

//----
bool Arm::grab(const Trans& T_target,
               const Trans& T_close)
{
    TipSt t; 

    //---- close in
    t.T = T_close;
    t.gripper = 1;
    auto& v = cfg_.dfltSpeed;
    moveTo(t, v);
    waitDone();

    //---- forward
    t.T = T_target;
    moveTo(t, v);
    waitDone();

    //---- grip close
    t.gripper = 0;
    moveTo(t, v);
    waitDone();

    return false; 
}

