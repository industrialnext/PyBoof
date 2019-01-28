import pyboof as pb
import numpy as np
import os
import glob

# Demonstration of how to calibrate a camera using a pinhole model
pb.init_memmap()

data_path = "../data/example/calibration/stereo/Bumblebee2_Chess/"


print("Configuring and creating a chessboard detector")
config = pb.ConfigFiducialChessboard(num_rows=5, num_cols=7, square_width=0.3)
detector = pb.FactoryFiducialCalibration.chessboard(config)

print("Detecting calibration targets")
observations = []
for file in glob.glob(os.path.join(data_path,"left*.jpg")):
    image = pb.load_single_band(file, np.float32)
    detector.detect(image)
    if detector.detected_points:
        print("success "+file)
        o = {"width": image.getWidth(),
             "height": image.getHeight(),
             "pixels": detector.detected_points}
        observations.append(o)
    else:
        print("failed "+file)

print("Solving for intrinsic parameters")

intrinsic,errors = pb.calibrate_pinhole(observations,detector,
                                        num_radial=2,tangential=True)

print()
print("Average Error {:.3f} pixels".format(sum([x["mean"] for x in errors])/len(errors)))
print(str(intrinsic))
