# CIS 520 Final Project
Michael Deng (michdeng@wharton)  
Samuel Ryan (samryan@seas)  
Mukund Venkateswaran (mukundv@seas)  
Kurt Convey (kconvey@seas)  


## How to Use
Upload the most up to date notebook from `clean_notebooks/` into [Google Colab](https://colab.research.google.com
 "Google Colab") and run all cells.

## Useful Links
[Overleaf Project Proposal](https://www.overleaf.com/5129544771bdtbmcqfddfs
 "Overleaf Project Proposal")

[Prelim Dataset](https://github.com/mukundv7/crvdataset
 "Initial Dataset")

[Paper on ML to detect corners](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5134517/
 "")


## Initial Results on Easier Dataset


#### Learning curves for a few different CNN models:
(implemented in PyTorch)
<img src="./assets/learning_curves.png" alt="Learning Curves" width="90%" />


#### Some examples of output during training:
The predictions get better as we progress through mini-batches.
<img src="./assets/chess_output.png" alt="Results image" width="90%" />


## Initial Preprocessing Results
Preprocessing code adapted from [here](https://github.com/Elucidation/ChessboardDetect/blob/master/FindChessboards.py
 "").


#### How Preprocessing Works:
1. Convert image to binary bitmap
2. Blur the image
3. [Sobol Filter](https://en.wikipedia.org/wiki/Sobel_operator)
4. [Canny Edge Detectors](https://en.wikipedia.org/wiki/Canny_edge_detector#Gaussian_filter)
5. [Finding Contours](https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html) with `cv2`
6. "Prune the contours"—[Ramer–Douglas–Peucker Algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) to reconcile "almost lines"
7. Find line intersections
8. Sanity checks
    * convex hull
    * correct num points
    * check angles between lines

<img src="./preprocessing/preprocessing_example.png" alt="Preprocessing" width="90%" />