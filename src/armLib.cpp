#include "arm/armLib.h"
#include "arm/armZ1.h"
#include "arm/armTcp.h"

using namespace arm;

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
        return mkSp<unitree::ArmZ1>();
#endif 

    log_e("Unkonw Arm type:'"+sModel+"'");
    return nullptr;

}

