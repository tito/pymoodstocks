//
//  ScannerViewController.m
//  moodstock
//
//  Created by Mathieu Virbel on 26/02/2015.
//
//

#import "ScannerViewController.h"

static int kMSResultTypes = MSResultTypeImage | MSResultTypeQRCode | MSResultTypeEAN13;

@interface ScannerViewController ()
@property IBOutlet UIView *videoPreview;
@property IBOutlet UINavigationItem *itemTitle;
@property IBOutlet UIBarButtonItem *itemButton;

@end

@implementation ScannerViewController

MSAutoScannerSession *_scannerSession;

- (IBAction)buttonClicked:(id)sender {
    [self.delegate buttonClicked];
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    _scannerSession = [[MSAutoScannerSession alloc] initWithScanner:_scanner];
    _scannerSession.delegate = self.delegate;
    _scannerSession.resultTypes = kMSResultTypes;
    
    CALayer *videoPreviewLayer = [self.videoPreview layer];
    [videoPreviewLayer setMasksToBounds:YES];
    
    CALayer *captureLayer = [_scannerSession captureLayer];
    [captureLayer setFrame:[self.videoPreview bounds]];
    
    [videoPreviewLayer insertSublayer:captureLayer
                                below:[[videoPreviewLayer sublayers] objectAtIndex:0]];
    [_scannerSession startRunning];
}

- (void)viewDidAppear:(BOOL)animated {
    [_scannerSession resumeProcessing];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
}

- (void)dealloc
{
    [_scannerSession stopRunning];
    [super dealloc];
}

- (void)updateInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    [_scannerSession setInterfaceOrientation:interfaceOrientation];
    
    AVCaptureVideoPreviewLayer *captureLayer = (AVCaptureVideoPreviewLayer *) [_scannerSession captureLayer];
    
    captureLayer.frame = self.view.bounds;
    
    // AVCapture orientation is the same as UIInterfaceOrientation
    switch (interfaceOrientation) {
        case UIInterfaceOrientationPortrait:
            [[captureLayer connection] setVideoOrientation:AVCaptureVideoOrientationPortrait];
            break;
        case UIInterfaceOrientationPortraitUpsideDown:
            [[captureLayer connection] setVideoOrientation:AVCaptureVideoOrientationPortraitUpsideDown];
            break;
        case UIInterfaceOrientationLandscapeLeft:
            [[captureLayer connection] setVideoOrientation:AVCaptureVideoOrientationLandscapeLeft];
            break;
        case UIInterfaceOrientationLandscapeRight:
            [[captureLayer connection] setVideoOrientation:AVCaptureVideoOrientationLandscapeRight];
            break;
        default:
            break;
    }
}

- (void)viewWillLayoutSubviews
{
    [self updateInterfaceOrientation:self.interfaceOrientation];
}
 
- (void)willAnimateRotationToInterfaceOrientation:(UIInterfaceOrientation)orientation duration:(NSTimeInterval)duration
{
    [super willAnimateRotationToInterfaceOrientation:orientation duration:duration];
    [self updateInterfaceOrientation:orientation];
}

- (void)setTitle:(NSString *)title {
    self.itemTitle.title = title;
}


@end
