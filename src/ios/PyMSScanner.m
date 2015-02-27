//
//  scanner.m
//  moodstock
//
//  Created by Mathieu Virbel on 26/02/2015.
//
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>
#import "ScannerViewController.h"
#import "PyMSScanner.h"

@implementation PyMSScanner

- (id) initWithApiKey:(NSString *)key secret:(NSString *)secret delegate:(NSObject *)delegate {
    self = [super init];
    _scannerVC = nil;
    _delegate = delegate;
    
    NSString *path = [MSScanner cachesPathFor:@"scanner.db"];
    _scanner = [[MSScanner alloc] init];
    [_scanner openWithPath:path key:key secret:secret error:nil];
    
    // Create the progression and completion blocks:
    void (^completionBlock)(MSSync *, NSError *) = ^(MSSync *op, NSError *error) {
        if (error)
            NSLog(@"Sync failed with error: %@", [error ms_message]);
        else
            NSLog(@"Sync succeeded (%li images(s))", (long)[_scanner count:nil]);
    };
    
    void (^progressionBlock)(NSInteger) = ^(NSInteger percent) {
        NSLog(@"Sync progressing: %li%%", (long)percent);
    };
    
    // Launch the synchronization
    [_scanner syncInBackgroundWithBlock:completionBlock progressBlock:progressionBlock];
    return self;
}

- (void) dealloc {
    NSLog(@"Scanner dealloc");
    [_scanner close:nil];
    [super dealloc];
}

- (void) setTitle:(NSString *)title {
    _title = title;
    if (_scannerVC != nil) {
        [_scannerVC setTitle:title];
    }
}

- (void) start {
    NSLog(@"Start the scanner");
    if (_scannerVC == nil) {
        _scannerVC = [[ScannerViewController alloc] init];
        _scannerVC.scanner = _scanner;
        _scannerVC.delegate = _delegate;
    }
    
    // get the current window
    UIApplication *app = [UIApplication sharedApplication];
    NSArray *windows = [app windows];
    UIWindow *window = [windows firstObject];
    UIViewController *controller = [window rootViewController];
    _controller = controller;
    [controller showViewController:_scannerVC sender:nil];
    if (_title != nil)
        [_scannerVC setTitle:_title];
}

- (void) stop {
    [_controller dismissViewControllerAnimated:YES completion:nil];
}

- (void) resume {
	if (_scannerVC != nil)
		[_scannerVC resume];
}

@end
