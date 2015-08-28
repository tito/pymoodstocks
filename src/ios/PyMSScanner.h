//
//  scanner.h
//  moodstock
//
//  Created by Mathieu Virbel on 26/02/2015.
//
//

#ifndef moodstock_scanner_h
#define moodstock_scanner_h

#import <Foundation/Foundation.h>
#import <CoreMotion/CoreMotion.h>
#import <Moodstocks/Moodstocks.h>
#import <UIKit/UIKit.h>
#import "ScannerViewController.h"


@protocol PyMSScannerDelegate <NSObject>

- (void)buttonClicked;

@end


@interface PyMSScanner : NSObject {
    MSScanner *_scanner;
    ScannerViewController *_scannerVC;
    UIViewController *_controller;
    int _popup;
    NSString *_title;
    NSObject *_delegate;
}

@end

#endif
