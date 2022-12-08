#include "arm/armLib.h"
#include "arm/armZ1.h"
#include "arm/armTcp.h"

using namespace arm;


//---- factory
Sp<Arm> Arm::create(const string& sModel)
{
    //--- check if remote
    size_t nf = sModel.find("robot://");
    if(nf!=string::npos)
    {
        string sUri = sModel.substr(nf);
        return mkSp<ArmTcp>(sUri);
    }

#ifdef WITH_ARM_Z1
    else if(sModel=="z1")
        return mkSp<unitree::ArmZ1>();
#endif 

    log_e("Unkonw Arm type:'"+sModel+"'");
    return nullptr;

}

