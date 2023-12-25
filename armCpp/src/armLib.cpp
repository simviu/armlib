#include "arm/armLib.h"

using namespace arm;

namespace{

    map<string, Arm::FuncCre> creators_;
}

//------
string Trans::str()const
{ 
    return "{\"t\":\""+vsn::str(t,3)+
           // "\", \"e\":\"" +e.str()+"\"}";  
           "\", \"q\":\"" +vsn::str(q)+"\"}";  

}

//----- TODO: deprecated
/*
bool Trans::set(const string& s)
{
    vector<double> ds;
    if(!s2data(s, ds, ',')) 
        return false;
    if(ds.size()<6) 
        return false;

    t << ds[0], ds[1], ds[2];

 //   e.rx = ds[3];
 //   e.ry = ds[4];
 //   e.rz = ds[5];
    return true;
}
*/
//----
string TipSt::str()const 
{ 
    return "{\"T\":"+ T.str() + 
        ", \"grip\":" + vsn::str(gripper) +"}"; 
}

//----
string ArmSt::str()const
{
    string sj;
    int N = angles.size();
    for(int i=0;i<N;i++)
        sj += ((i==0)?"":",")+::str(angles[i]);
    string s = "{ \"tip\":"+tip.str() + 
               ", \"angles\":["+sj+"] }";
    return s;
        
}

//---- factory
Sp<Arm> Arm::create(const string& sModel)
{
    if(sModel=="dummy")
        return mkSp<Arm>();
    
    auto it = creators_.find(sModel);
    if(it!=creators_.end())
        return (it->second)();
    
    log_e("No creator found for '"+sModel+"'");

    return nullptr;

}
//----
void Arm::addCreator(const string& sModel, FuncCre f)
{
    creators_[sModel] = f;
}
//----
void Arm::waitDone()
{
    sys::sleep(0.05);
    while(!done())
        sys::sleep(0.01);
}

//----
bool Arm::grab(const Trans& T_target,
               const vec3& dt0)
{
    TipSt t; 

    //---- Approach
    t.T = T_target;
    t.T.t += dt0;
    t.gripper = 1;
    auto& v = cfg_.dfltSpeed;
    moveTo(t, v);
    waitDone();
    //sys::sleep(1);

    //---- forward
    t.T = T_target;
    moveTo(t, v);
    waitDone();

    //sys::sleep(1);
    //---- grip close
    t.gripper = 0;
    moveTo(t, v);
    waitDone();
    //sys::sleep(1);
    
    return true; 
}

