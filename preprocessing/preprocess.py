from preprocessing import *
from tqdm import tqdm
# import sys
# import traceback

# class TracePrints(object):
#   def __init__(self):    
#     self.stdout = sys.stdout
#   def write(self, s):
#     self.stdout.write("Writing %r\n" % s)
#     traceback.print_stack(file=self.stdout)

# sys.stdout = TracePrints()

def main_with_warped(glob_path):
    filenames = glob.glob(glob_path)
    filenames = sorted(filenames)
    print(f"Files: {filenames}")
  
    if (len(filenames) == 0):
        print("No files found.")
        return
    
    with tqdm(total=len(filenames), 
            desc=f'Files from {glob_path}', 
            unit=' file',
            disable=False) as pbar:
        for i,filename in enumerate(filenames):
            pbar.set_postfix(current_file=filename, refresh=True),
            pbar.update(1)
            

            img, img_orig = loadImage(filename)
            M, ideal_grid, grid_next, grid_good, spts = findChessboard(img)
            # View
            if M is not None:
                # generate mapping for warping image
                M, _ = generateNewBestFit((ideal_grid+8)*32, grid_next, 
                                          grid_good) 
                img_warp = cv2.warpPerspective(img, M, (17*32, 17*32), 
                                               flags=cv2.WARP_INVERSE_MAP)

                best_lines_x, best_lines_y = getBestLines(img_warp)

                xy_unwarp = getUnwarpedPoints(best_lines_x, best_lines_y, M)
                board_outline_unwarp = getBoardOutline(best_lines_x, best_lines_y, M)

                # show warped
                side_len = 2048
                pts_dest = np.array([[0,side_len],[side_len,side_len],[side_len,0],[0,0]])

                # calculate homography
                h, status = cv2.findHomography(board_outline_unwarp[0:4], pts_dest)
                im_out = cv2.warpPerspective(np.squeeze(img), h, (side_len,side_len))
                # show warped
                fig = plt.figure(frameon=False)
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                ax.imshow(im_out, cmap='Greys_r');
                axis('off')
                fname = filename.split('.')[-2].split('/')[-1]
                save_dest = f'warped_training_images/{fname}.png'
                plt.savefig(save_dest, bbox_inches='tight', pad_inches=0)

            else:
                print(f'Could not preprocess: {filename}')
        

if __name__ == '__main__':
    # main_with_warped('training_images/IMG_*.JPG')
    main_with_warped('real_images_tr/labeled/*.jpeg')