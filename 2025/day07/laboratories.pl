% Day 7: Laboratories - Prolog solution for tachyon beam simulation
% Simulate beam splitting through manifold

% Load manifold from file
load_manifold(Filename, Grid, StartCol) :-
    open(Filename, read, Stream),
    read_lines(Stream, Lines),
    close(Stream),
    maplist(atom_chars, Lines, Grid),
    find_start_position(Grid, StartCol).

% Read all lines from stream
read_lines(Stream, Lines) :-
    read_line_to_codes(Stream, Codes),
    (   Codes == end_of_file
    ->  Lines = []
    ;   atom_codes(Line, Codes),
        Lines = [Line|RestLines],
        read_lines(Stream, RestLines)
    ).

% Find starting position 'S'
find_start_position(Grid, StartCol) :-
    Grid = [FirstRow|_],
    nth0(StartCol, FirstRow, 'S').

% Get grid dimensions
grid_dimensions(Grid, Rows, Cols) :-
    length(Grid, Rows),
    (   Grid = [FirstRow|_]
    ->  length(FirstRow, Cols)
    ;   Cols = 0
    ).

% Get cell value at position (R, C)
get_cell(Grid, R, C, Value) :-
    grid_dimensions(Grid, Rows, Cols),
    R >= 0, R < Rows,
    C >= 0, C < Cols,
    nth0(R, Grid, Row),
    nth0(C, Row, Value).

% Check if position is within grid bounds
in_bounds(Grid, R, C) :-
    grid_dimensions(Grid, Rows, Cols),
    R >= 0, R < Rows,
    C >= 0, C < Cols.

% Part 1: Count beam splits
part1(Grid, StartCol, SplitCount) :-
    simulate_beams(Grid, StartCol, SplitCount).

% Simulate beam movement and count splits
simulate_beams(Grid, StartCol, SplitCount) :-
    InitialBeams = [beam(1, StartCol)],  % Start at row 1 (after S)
    simulate_step(Grid, InitialBeams, 0, SplitCount).

% Simulate one step of beam movement
simulate_step(_, [], SplitCount, SplitCount) :- !.  % No more beams
simulate_step(Grid, Beams, CurrentSplits, FinalSplits) :-
    move_beams(Grid, Beams, NewBeams, NewSplits),
    TotalSplits is CurrentSplits + NewSplits,
    simulate_step(Grid, NewBeams, TotalSplits, FinalSplits).

% Move all beams one step down
move_beams(_, [], [], 0).
move_beams(Grid, [beam(R, C)|RestBeams], NewBeams, TotalSplits) :-
    NextR is R + 1,
    (   in_bounds(Grid, NextR, C)
    ->  get_cell(Grid, NextR, C, Cell),
        handle_beam_at_cell(Cell, NextR, C, BeamResults, Splits),
        move_beams(Grid, RestBeams, RestNewBeams, RestSplits),
        append(BeamResults, RestNewBeams, NewBeams),
        TotalSplits is Splits + RestSplits
    ;   % Beam exits grid
        move_beams(Grid, RestBeams, NewBeams, TotalSplits)
    ).

% Handle beam interaction with cell
handle_beam_at_cell('.', R, C, [beam(R, C)], 0) :- !.  % Continue through empty space
handle_beam_at_cell('^', R, C, [beam(R, LeftC), beam(R, RightC)], 1) :-  % Split at splitter
    LeftC is C - 1,
    RightC is C + 1.

% Merge beams at same position (remove duplicates)
merge_beams(Beams, MergedBeams) :-
    sort(Beams, MergedBeams).

% Part 2: Count total timeline paths
part2(Grid, StartCol, TimelineCount) :-
    count_timelines(Grid, 1, StartCol, TimelineCount).

% Count timeline paths using memoization
:- dynamic(timeline_memo/3).

count_timelines(Grid, R, C, Count) :-
    timeline_memo(R, C, Count), !.
count_timelines(Grid, R, C, Count) :-
    count_timelines_helper(Grid, R, C, Count),
    assertz(timeline_memo(R, C, Count)).

count_timelines_helper(Grid, R, C, Count) :-
    (   \+ in_bounds(Grid, R, C)
    ->  Count = 1  % Beam exits - one timeline
    ;   get_cell(Grid, R, C, Cell),
        NextR is R + 1,
        (   Cell == '^'
        ->  % Timeline splits
            LeftC is C - 1,
            RightC is C + 1,
            count_timelines(Grid, NextR, LeftC, LeftCount),
            count_timelines(Grid, NextR, RightC, RightCount),
            Count is LeftCount + RightCount
        ;   % Continue straight
            count_timelines(Grid, NextR, C, Count)
        )
    ).

% Clear memoization
clear_memo :-
    retractall(timeline_memo(_, _, _)).

% Alternative: Find all actual timeline paths (for debugging)
find_all_timelines(Grid, StartCol, Timelines) :-
    findall(Timeline, 
            timeline_path(Grid, 1, StartCol, [pos(1, StartCol)], Timeline),
            Timelines).

% Generate a single timeline path
timeline_path(Grid, R, C, Path, FinalPath) :-
    (   \+ in_bounds(Grid, R, C)
    ->  reverse(Path, FinalPath)  % Beam exits
    ;   get_cell(Grid, R, C, Cell),
        NextR is R + 1,
        (   Cell == '^'
        ->  % Choose left or right branch
            (   LeftC is C - 1,
                timeline_path(Grid, NextR, LeftC, [pos(NextR, LeftC)|Path], FinalPath)
            ;   RightC is C + 1,
                timeline_path(Grid, NextR, RightC, [pos(NextR, RightC)|Path], FinalPath)
            )
        ;   % Continue straight
            timeline_path(Grid, NextR, C, [pos(NextR, C)|Path], FinalPath)
        )
    ).

% Display grid
display_grid(Grid) :-
    forall(member(Row, Grid),
           (atomic_list_concat(Row, '', RowStr),
            format('~w~n', [RowStr]))).

% Test predicates
test_example :-
    load_manifold('example.txt', Grid, StartCol),
    part1(Grid, StartCol, Splits),
    format('Part 1 (example): ~w splits~n', [Splits]),
    clear_memo,
    part2(Grid, StartCol, Timelines),
    format('Part 2 (example): ~w timelines~n', [Timelines]).

test_main :-
    load_manifold('input.txt', Grid, StartCol),
    part1(Grid, StartCol, Splits),
    format('Part 1: ~w splits~n', [Splits]),
    clear_memo,
    part2(Grid, StartCol, Timelines),
    format('Part 2: ~w timelines~n', [Timelines]).

% Debug: Show beam simulation step by step
debug_simulation(Filename) :-
    load_manifold(Filename, Grid, StartCol),
    format('Starting simulation at column ~w~n', [StartCol]),
    InitialBeams = [beam(1, StartCol)],
    debug_simulate_step(Grid, InitialBeams, 1, 0).

debug_simulate_step(_, [], Step, TotalSplits) :-
    format('Simulation complete at step ~w. Total splits: ~w~n', [Step, TotalSplits]).
debug_simulate_step(Grid, Beams, Step, CurrentSplits) :-
    length(Beams, BeamCount),
    format('Step ~w: ~w beams active~n', [Step, BeamCount]),
    forall(member(beam(R, C), Beams),
           format('  Beam at (~w, ~w)~n', [R, C])),
    move_beams(Grid, Beams, NewBeams, NewSplits),
    TotalSplits is CurrentSplits + NewSplits,
    (   NewSplits > 0
    ->  format('  ~w new splits occurred~n', [NewSplits])
    ;   true
    ),
    NextStep is Step + 1,
    debug_simulate_step(Grid, NewBeams, NextStep, TotalSplits).

% Debug: Show some timeline paths
show_timelines(Filename, MaxCount) :-
    load_manifold(Filename, Grid, StartCol),
    find_all_timelines(Grid, StartCol, AllTimelines),
    length(AllTimelines, TotalCount),
    format('Found ~w total timelines~n', [TotalCount]),
    take(MaxCount, AllTimelines, SomeTimelines),
    forall(member(Timeline, SomeTimelines),
           (format('Timeline: '),
            forall(member(pos(R, C), Timeline),
                   format('(~w,~w) ', [R, C])),
            nl)).

% Utility: take first N elements
take(0, _, []) :- !.
take(_, [], []) :- !.
take(N, [H|T], [H|Result]) :-
    N > 0,
    N1 is N - 1,
    take(N1, T, Result).