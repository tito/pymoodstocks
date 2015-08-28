//
//  ScannerViewController.h
//  moodstock
//
//  Created by Mathieu Virbel on 26/02/2015.
//
//

#import <UIKit/UIKit.h>
#import <Moodstocks/Moodstocks.h>

@interface ScannerViewController : UIViewController

@property(assign) MSScanner *scanner;
@property(assign) id delegate;

@end
