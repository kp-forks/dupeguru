/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "PyResultTable.h"
#import "PyStatsLabel.h"
#import "PyApp.h"

@interface PyDupeGuruBase : PyApp
- (void)bindCocoa:(id)cocoa;
- (PyResultTable *)resultTable;
- (PyStatsLabel *)statsLabel;
//Actions
- (NSNumber *)addDirectory:(NSString *)name;
- (void)loadResultsFrom:(NSString *)filename;
- (void)saveResultsAs:(NSString *)filename;
- (void)loadSession;
- (void)saveSession;
- (void)clearIgnoreList;
- (void)purgeIgnoreList;
- (NSString *)exportToXHTML;
- (void)invokeCommand:(NSString *)cmd;

- (void)doScan;

- (void)toggleSelectedMark;
- (void)markAll;
- (void)markInvert;
- (void)markNone;

- (void)addSelectedToIgnoreList;
- (void)openSelected;
- (void)revealSelected;
- (void)makeSelectedReference;
- (void)applyFilter:(NSString *)filter;

- (void)copyOrMove:(NSNumber *)aCopy markedTo:(NSString *)destination recreatePath:(NSNumber *)aRecreateType;
- (void)deleteMarked;
- (void)hardlinkMarked;
- (void)removeMarked;

//Data
- (NSNumber *)getIgnoreListCount;
- (NSNumber *)getMarkCount;
- (BOOL)scanWasProblematic;
- (BOOL)resultsAreModified;

//Scanning options
- (void)setScanType:(NSNumber *)scan_type;
- (void)setMinMatchPercentage:(NSNumber *)percentage;
- (void)setMixFileKind:(BOOL)mix_file_kind;
- (void)setEscapeFilterRegexp:(BOOL)escape_filter_regexp;
- (void)setRemoveEmptyFolders:(BOOL)remove_empty_folders;
- (void)setIgnoreHardlinkMatches:(BOOL)ignore_hardlink_matches;
- (void)setSizeThreshold:(NSInteger)size_threshold;
@end
