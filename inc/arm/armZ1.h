#pragma once

#include "arm/armLib.h"

using namespace arm;

#ifdef WITH_ARM_Z1

#include "unitree_arm_sdk/control/unitreeArm.h"

namespace UNITREE_ARM
{
    //----
    class ArmZ1 : public Arm
    {
    public:
        ArmZ1()
        {
        //    pCtrlComp_ = new CtrlComponents(0.002, true);
            p_uarm_ = new unitreeArm(true);
        }

        virtual bool init()override;
        virtual bool moveTo(const TipSt& ts, float spd) override;
        virtual bool getSt(ArmSt& st) override; 
        virtual bool test()override;
        virtual bool play(const string& sf)override;
        virtual bool done()const override;
    protected:
        //CtrlComponents* pCtrlComp_ = nullptr;
        unitreeArm* p_uarm_ = nullptr;
    };
}

#endif // #ifdef WITH_ARM_Z1
