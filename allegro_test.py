from move_dexarm import DexArmControl

arm_controller = DexArmControl()

curr_pos = arm_controller.allegro.current_joint_pose.position

print(curr_pos)

desired_pos = []

arm_controller.move_hand(desired_pos)

