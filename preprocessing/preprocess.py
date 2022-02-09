'''
Preprocessing Main

'''

from preprocessing import *
from tqdm import tqdm
import click
import glob

def process_image(filename, dest_path, verbose, plot_original=False):
    img, img_orig = loadImage(filename)
    # print(np.shape(img))
    # print(np.shape(img_orig))
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

        side_len = 2048
        myDPI = 192
        pts_dest = np.array([[0,side_len],[side_len,side_len],[side_len,0],[0,0]])

        # calculate homography
        h, status = cv2.findHomography(board_outline_unwarp[0:4], pts_dest)
        
        im_out = cv2.warpPerspective(np.squeeze(img_orig), h, (side_len,side_len))
        
        # write warped to file
        # fig = plt.figure(frameon=False, figsize=(side_len/myDPI,side_len/myDPI))
        fig = plt.figure(frameon=False, figsize=(30,30))
        im_plot = imshow(im_out, cmap='Greys_r', aspect='auto')
        ax = plt.gca()
        ax.set_axis_off()
        fname = filename.split('.')[-2].split('/')[-1]
        save_dest = f'{dest_path}/{fname}.png'
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        plt.savefig(save_dest, bbox_inches=extent, pad_inches=0)
        
        if plot_original:
            fig = plt.figure(frameon=False, figsize=(30, 42))
            im_plot = imshow(img_orig, cmap='Greys_r', aspect='auto')
            plt.plot(board_outline_unwarp[:,0], board_outline_unwarp[:,1], 'ro-', markersize=5, linewidth=5)

            ax = plt.gca()
            ax.set_axis_off()
            fname = filename.split('.')[-2].split('/')[-1]
            save_dest = f'{dest_path}/ORIGINAL_{fname}.png'
            extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            plt.savefig(save_dest, bbox_inches=extent, pad_inches=0)

    else:
        print(f'Could not preprocess: {filename}')


@click.command()
@click.option('--glob_path', prompt=True,
              help='Path to directory with images to preprocess')
@click.option('--dest_path', prompt=True, help='Path to directory to put '
                                              f'output. e.g. '
                                              f'warped_training_images')
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def main_with_warped(glob_path, dest_path, verbose):
    filenames = glob.glob(glob_path)[::10]
    #filenames = sorted(filenames)
    # print(f"Files: {filenames}")
  
    if (len(filenames) == 0):
        print("No files found.")
        return
    else:
        print(f"Found {len(filenames)} files.")
    
    with tqdm(total=len(filenames), 
            desc=f'Files from {glob_path}', 
            unit=' file',
            disable=False) as pbar:
        for i,filename in enumerate(filenames):
            pbar.set_postfix(current_file=filename, refresh=True),
            pbar.update(1)
            process_image(filename, dest_path, verbose)
        

if __name__ == '__main__':
    main_with_warped()
