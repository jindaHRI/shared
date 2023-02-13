from move_dexarm import DexArmControl

arm_controller = DexArmControl()

curr_pos = arm_controller.allegro.current_joint_pose.position

print(curr_pos)

desired_pos = []

arm_controller.move_hand(desired_pos)




    def new_coords(self, coord1, coord2):
        vec = coord1 - coord2
        mid = (coord1 + coord2)/2
        d = np.linalg.norm(vec)
        vec = vec/d
        new_coord1 = r*d/2*vec+mid
        new_coord2 = r*d/2*(-vec)+mid
    
        return new_coord1, new_coord2
        
    def dilate_bounds(self, thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds):
        r = 1.2 #enlarge rate
                
        top_right = thumb_index_bounds[0]
        bottom_right = thumb_index_bounds[1]
        
        index_top = thumb_index_bounds[2]
        index_bot = thumb_index_bounds[3]
        
        index_z_u = thumb_index_bounds[4][0]
        index_z_l = thumb_index_bounds[4][1]
        
        middle_top = thumb_middle_bounds[2]
        middle_bot = thumb_middle_bounds[3]                
        
        middle_z_u = thumb_middle_bounds[4][0]
        middle_z_l = thumb_middle_bounds[4][1]
        
        ring_top = thumb_ring_bounds[2]
        ring_bot = thumb_ring_bounds[3]
        
        ring_z_u = thumb_ring_bounds[4][0]
        ring_z_l = thumb_ring_bounds[4][1]
        
        #enlargement
        new_index_top, new_index_bot = self.new_coords(index_top, index_bot)
        new_middle_top, new_middle_bot = self.new_coords(middle_top, middle_bot)
        new_ring_top, new_ring_bot = self.new_coords(ring_top, ring_bot)
        
        new_index_z_u, new_index_z_l = self.new_coords(index_z_u, index_z_l)
        new_middle_z_u, new_middle_z_l = self.new_coords(middle_z_u, middle_z_l)
        new_ring_z_u, new_ring_z_l = self.new_coords(ring_z_u, ring_z_l)
                
        new_top_right, _ = self.new_coords(top_right, index_bot)
        new_bottom_right, _ = self.new_coords(bottom_right, index_top)
                
        #assign results
        thumb_index_bounds = np.vstack((new_top_right, new_bottom_right, new_index_top, new_index_bot, np.array([new_index_z_u, new_index_z_l]))
        thumb_middle_bounds = np.vstack((new_index_top, new_index_bot, new_middle_bot, new_middle_top, np.array([new_middle_z_u, new_middle_z_l]))
        thumb_ring_bounds = np.vstack((new_middle_top, new_middle_bot, new_ring_bot, new_ring_top, np.array([new_ring_z_u, new_ring_z_l]))
        
        
        return thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds
        
    

    def get_bounds(self):
        sys.stdin = open(0) # To take inputs while spawning multiple processes

        if check_file(VR_THUMB_BOUNDS_PATH):
            use_calibration_file = input("\nCalibration file already exists. Do you want to create a new one? Press y for Yes else press Enter")

            if use_calibration_file == "y":
                thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds = self._calibrate()
            else:
                calibrated_bounds = np.load(VR_THUMB_BOUNDS_PATH)
                thumb_index_bounds = calibrated_bounds[:5]
                thumb_middle_bounds = calibrated_bounds[5:10]
                thumb_ring_bounds = calibrated_bounds[10:]        
        else:
            print("\nNo calibration file found. Need to calibrate hand poses.\n")
            thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds = self._calibrate()
            
        thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds = self.dilate_bounds(thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds)

        return thumb_index_bounds, thumb_middle_bounds, thumb_ring_bounds

