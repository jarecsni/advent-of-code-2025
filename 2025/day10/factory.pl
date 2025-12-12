% Day 10: Factory - Prolog solution using constraint logic programming
% Solve indicator light configuration using minimum button presses

:- use_module(library(clpfd)).

% Parse a machine specification line
% Format: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
parse_machine(Line, machine(Target, Buttons, _Joltage)) :-
    % Extract target pattern [.##.]
    sub_atom(Line, Start, Len, _, Target),
    sub_atom(Target, 0, 1, _, '['),
    sub_atom(Target, _, 1, 0, ']'),
    !,
    % Extract button definitions (everything between ] and {)
    atom_concat(_, Rest1, Line),
    sub_atom(Rest1, BStart, _, _, '] '),
    sub_atom(Rest1, BStart, BLen, _, ButtonsStr),
    sub_atom(ButtonsStr, 0, BLen2, _, ButtonsStr2),
    sub_atom(ButtonsStr2, _, 1, 0, ' {'),
    BLen2 is BLen - 2,
    % Parse buttons
    parse_buttons(ButtonsStr2, Buttons).

% Parse button definitions like "(3) (1,3) (2) (2,3) (0,2) (0,1)"
parse_buttons(Str, Buttons) :-
    atom_chars(Str, Chars),
    phrase(buttons(Buttons), Chars).

% DCG for parsing buttons
buttons([Button|Rest]) --> button(Button), !, buttons(Rest).
buttons([]) --> [].

button(Indices) --> 
    ['('], 
    indices(Indices), 
    [')'], 
    optional_space.

indices([I|Rest]) --> 
    digit_sequence(I), 
    [','], !, 
    indices(Rest).
indices([I]) --> 
    digit_sequence(I).

digit_sequence(N) --> 
    digit(D), 
    { N is D }.
digit_sequence(N) --> 
    digit(D1), 
    digit(D2), 
    { N is D1 * 10 + D2 }.

digit(0) --> ['0'].
digit(1) --> ['1'].
digit(2) --> ['2'].
digit(3) --> ['3'].
digit(4) --> ['4'].
digit(5) --> ['5'].
digit(6) --> ['6'].
digit(7) --> ['7'].
digit(8) --> ['8'].
digit(9) --> ['9'].

optional_space --> [' '], !.
optional_space --> [].

% Convert target pattern to binary list
target_to_binary(Target, Binary) :-
    atom_chars(Target, Chars),
    include(light_char, Chars, LightChars),
    maplist(char_to_bit, LightChars, Binary).

light_char(C) :- member(C, ['.', '#']).

char_to_bit('.', 0).
char_to_bit('#', 1).

% Solve a single machine using constraint logic programming
solve_machine(machine(TargetAtom, Buttons, _), ButtonPresses, MinPresses) :-
    target_to_binary(TargetAtom, Target),
    length(Target, NumLights),
    length(Buttons, NumButtons),
    
    % Create binary variables for button presses
    length(ButtonPresses, NumButtons),
    ButtonPresses ins 0..1,
    
    % Create constraints for each light
    create_light_constraints(Target, Buttons, ButtonPresses, 0),
    
    % Minimize total button presses
    sum(ButtonPresses, #=, MinPresses),
    
    % Find optimal solution
    labeling([min(MinPresses)], ButtonPresses).

% Create constraint for each light position
create_light_constraints([], _, _, _).
create_light_constraints([TargetBit|RestTarget], Buttons, ButtonPresses, LightIndex) :-
    % Find which buttons affect this light
    find_affecting_buttons(Buttons, ButtonPresses, LightIndex, 0, AffectingPresses),
    
    % Sum of affecting button presses must equal target (mod 2)
    sum(AffectingPresses, #=, Sum),
    Sum mod 2 #= TargetBit,
    
    NextIndex is LightIndex + 1,
    create_light_constraints(RestTarget, Buttons, ButtonPresses, NextIndex).

% Find button presses that affect a specific light
find_affecting_buttons([], [], _, _, []).
find_affecting_buttons([ButtonIndices|RestButtons], [Press|RestPresses], LightIndex, ButtonIndex, [Press|RestAffecting]) :-
    member(LightIndex, ButtonIndices), !,
    NextButtonIndex is ButtonIndex + 1,
    find_affecting_buttons(RestButtons, RestPresses, LightIndex, NextButtonIndex, RestAffecting).
find_affecting_buttons([_|RestButtons], [_|RestPresses], LightIndex, ButtonIndex, Affecting) :-
    NextButtonIndex is ButtonIndex + 1,
    find_affecting_buttons(RestButtons, RestPresses, LightIndex, NextButtonIndex, Affecting).

% Solve all machines and sum minimum presses
solve_all_machines(Machines, TotalPresses) :-
    solve_machines(Machines, AllPresses),
    sum_list(AllPresses, TotalPresses).

solve_machines([], []).
solve_machines([Machine|RestMachines], [MinPresses|RestPresses]) :-
    solve_machine(Machine, _, MinPresses),
    solve_machines(RestMachines, RestPresses).

% Main predicate to solve from file
solve_factory(Filename, TotalPresses) :-
    read_file_to_codes(Filename, Codes),
    atom_codes(Content, Codes),
    atomic_list_concat(Lines, '\n', Content),
    exclude(=(''), Lines, NonEmptyLines),
    maplist(parse_machine, NonEmptyLines, Machines),
    solve_all_machines(Machines, TotalPresses).

% Test with example
test_example :-
    solve_factory('example.txt', Total),
    format('Example total: ~w~n', [Total]).

% Solve main input
solve_main :-
    solve_factory('input.txt', Total),
    format('Main total: ~w~n', [Total]).

% Simple test case
test_simple :-
    Machine = machine('[.##.]', [[3], [1,3], [2], [2,3], [0,2], [0,1]], [3,5,4,7]),
    solve_machine(Machine, Presses, MinPresses),
    format('Button presses: ~w, Total: ~w~n', [Presses, MinPresses]).