% Day 4: Printing Department - Prolog solution for paper roll accessibility
% Count accessible rolls and simulate iterative removal

% Load grid from file
load_grid(Filename, Grid) :-
    open(Filename, read, Stream),
    read_lines(Stream, Lines),
    close(Stream),
    maplist(atom_chars, Lines, Grid).

% Read all lines from stream
read_lines(Stream, Lines) :-
    read_line_to_codes(Stream, Codes),
    (   Codes == end_of_file
    ->  Lines = []
    ;   atom_codes(Line, Codes),
        Lines = [Line|RestLines],
        read_lines(Stream, RestLines)
    ).

% Get grid dimensions
grid_dimensions(Grid, Rows, Cols) :-
    length(Grid, Rows),
    (   Grid = [FirstRow|_]
    ->  length(FirstRow, Cols)
    ;   Cols = 0
    ).

% Get cell value at position (R, C)
get_cell(Grid, R, C, Value) :-
    nth0(R, Grid, Row),
    nth0(C, Row, Value).

% Set cell value at position (R, C)
set_cell(Grid, R, C, NewValue, NewGrid) :-
    nth0(R, Grid, Row),
    replace_nth0(C, Row, NewValue, NewRow),
    replace_nth0(R, Grid, NewRow, NewGrid).

% Replace element at index N in list
replace_nth0(0, [_|T], NewValue, [NewValue|T]) :- !.
replace_nth0(N, [H|T], NewValue, [H|NewT]) :-
    N > 0,
    N1 is N - 1,
    replace_nth0(N1, T, NewValue, NewT).

% Get all 8 neighbors (Moore neighborhood)
neighbors(R, C, Neighbors) :-
    findall([NR, NC], 
            (member(DR, [-1, 0, 1]),
             member(DC, [-1, 0, 1]),
             \+ (DR == 0, DC == 0),
             NR is R + DR,
             NC is C + DC),
            Neighbors).

% Count paper rolls ('@') in neighborhood
count_neighbor_rolls(Grid, R, C, Count) :-
    neighbors(R, C, NeighborCoords),
    include(is_roll_at(Grid), NeighborCoords, RollNeighbors),
    length(RollNeighbors, Count).

% Check if position has a paper roll
is_roll_at(Grid, [R, C]) :-
    grid_dimensions(Grid, Rows, Cols),
    R >= 0, R < Rows,
    C >= 0, C < Cols,
    get_cell(Grid, R, C, '@').

% Check if a roll is accessible (< 4 neighboring rolls)
is_accessible(Grid, R, C) :-
    get_cell(Grid, R, C, '@'),
    count_neighbor_rolls(Grid, R, C, Count),
    Count < 4.

% Find all accessible rolls in grid
find_accessible_rolls(Grid, AccessibleRolls) :-
    grid_dimensions(Grid, Rows, Cols),
    Rows1 is Rows - 1,
    Cols1 is Cols - 1,
    findall([R, C],
            (between(0, Rows1, R),
             between(0, Cols1, C),
             is_accessible(Grid, R, C)),
            AccessibleRolls).

% Part 1: Count accessible rolls
part1(Grid, Count) :-
    find_accessible_rolls(Grid, AccessibleRolls),
    length(AccessibleRolls, Count).

% Remove accessible rolls from grid
remove_accessible_rolls(Grid, NewGrid) :-
    find_accessible_rolls(Grid, AccessibleRolls),
    remove_rolls(Grid, AccessibleRolls, NewGrid).

% Remove specific rolls from grid
remove_rolls(Grid, [], Grid).
remove_rolls(Grid, [[R, C]|RestRolls], FinalGrid) :-
    set_cell(Grid, R, C, '.', NewGrid),
    remove_rolls(NewGrid, RestRolls, FinalGrid).

% Part 2: Iteratively remove accessible rolls until no more can be removed
part2(Grid, TotalRemoved) :-
    part2_helper(Grid, 0, TotalRemoved).

part2_helper(Grid, Acc, TotalRemoved) :-
    find_accessible_rolls(Grid, AccessibleRolls),
    length(AccessibleRolls, Count),
    (   Count == 0
    ->  TotalRemoved = Acc
    ;   remove_accessible_rolls(Grid, NewGrid),
        NewAcc is Acc + Count,
        part2_helper(NewGrid, NewAcc, TotalRemoved)
    ).

% Count total rolls in grid
count_total_rolls(Grid, Count) :-
    grid_dimensions(Grid, Rows, Cols),
    Rows1 is Rows - 1,
    Cols1 is Cols - 1,
    findall([R, C],
            (between(0, Rows1, R),
             between(0, Cols1, C),
             get_cell(Grid, R, C, '@')),
            Rolls),
    length(Rolls, Count).

% Display grid
display_grid(Grid) :-
    forall(member(Row, Grid),
           (atomic_list_concat(Row, '', RowStr),
            format('~w~n', [RowStr]))).

% Test predicates
test_example :-
    load_grid('example.txt', Grid),
    part1(Grid, Count1),
    format('Part 1 (example): ~w accessible rolls~n', [Count1]),
    part2(Grid, Count2),
    format('Part 2 (example): ~w total removed rolls~n', [Count2]).

test_main :-
    load_grid('input.txt', Grid),
    part1(Grid, Count1),
    format('Part 1: ~w accessible rolls~n', [Count1]),
    part2(Grid, Count2),
    format('Part 2: ~w total removed rolls~n', [Count2]).

% Debug: Show accessible rolls
show_accessible(Filename) :-
    load_grid(Filename, Grid),
    find_accessible_rolls(Grid, AccessibleRolls),
    length(AccessibleRolls, Count),
    format('Found ~w accessible rolls:~n', [Count]),
    forall(member([R, C], AccessibleRolls),
           format('  Roll at (~w, ~w)~n', [R, C])).

% Debug: Show grid with accessible rolls marked
show_marked_grid(Filename) :-
    load_grid(Filename, Grid),
    find_accessible_rolls(Grid, AccessibleRolls),
    mark_accessible_rolls(Grid, AccessibleRolls, MarkedGrid),
    display_grid(MarkedGrid).

% Mark accessible rolls with 'X'
mark_accessible_rolls(Grid, [], Grid).
mark_accessible_rolls(Grid, [[R, C]|RestRolls], FinalGrid) :-
    set_cell(Grid, R, C, 'X', NewGrid),
    mark_accessible_rolls(NewGrid, RestRolls, FinalGrid).

% Simulate one step of removal
simulate_step(Grid, NewGrid, RemovedCount) :-
    find_accessible_rolls(Grid, AccessibleRolls),
    length(AccessibleRolls, RemovedCount),
    remove_accessible_rolls(Grid, NewGrid).

% Debug: Show step-by-step simulation
show_simulation(Filename) :-
    load_grid(Filename, Grid),
    show_simulation_steps(Grid, 1).

show_simulation_steps(Grid, Step) :-
    find_accessible_rolls(Grid, AccessibleRolls),
    length(AccessibleRolls, Count),
    (   Count == 0
    ->  format('Simulation complete after ~w steps~n', [Step1]),
        Step1 is Step - 1
    ;   format('Step ~w: Removing ~w rolls~n', [Step, Count]),
        remove_accessible_rolls(Grid, NewGrid),
        NextStep is Step + 1,
        show_simulation_steps(NewGrid, NextStep)
    ).