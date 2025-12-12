% Day 11: Reactor - Prolog solution for graph path counting
% Find all paths through electrical device network

% Dynamic predicates for the graph
:- dynamic(edge/2).
:- dynamic(path_count_memo/3).

% Parse input file and assert edges
load_graph(Filename) :-
    retractall(edge(_, _)),
    retractall(path_count_memo(_, _, _)),
    open(Filename, read, Stream),
    read_lines(Stream, Lines),
    close(Stream),
    maplist(parse_line, Lines).

% Read all lines from stream
read_lines(Stream, Lines) :-
    read_line_to_codes(Stream, Codes),
    (   Codes == end_of_file
    ->  Lines = []
    ;   atom_codes(Line, Codes),
        Lines = [Line|RestLines],
        read_lines(Stream, RestLines)
    ).

% Parse a line like "you: bbb ccc"
parse_line(Line) :-
    atom_length(Line, Len),
    Len > 0,
    \+ sub_atom(Line, 0, 1, _, '#'),  % Skip comments
    sub_atom(Line, ColonPos, 1, _, ':'), !,  % Find colon position
    sub_atom(Line, 0, ColonPos, _, From),
    ColonPos1 is ColonPos + 2,  % Skip ': '
    RestLen is Len - ColonPos1,
    sub_atom(Line, ColonPos1, RestLen, _, ToList),
    atomic_list_concat(ToAtoms, ' ', ToList),
    exclude(=(''), ToAtoms, NonEmptyAtoms),  % Remove empty atoms
    maplist(assert_edge(From), NonEmptyAtoms).
parse_line(_).  % Skip invalid lines

% Assert edge from From to To
assert_edge(From, To) :-
    To \== '',  % Skip empty atoms
    assertz(edge(From, To)).

% Part 1: Count all paths from 'you' to 'out'
part1(Count) :-
    count_paths(you, out, Count).

% Part 2: Count paths from 'svr' to 'out' that visit both 'fft' and 'dac'
part2(Count) :-
    count_paths_with_requirements(svr, out, [fft, dac], Count).

% Count simple paths between two nodes (with memoization)
count_paths(From, To, Count) :-
    path_count_memo(From, To, Count), !.
count_paths(From, To, Count) :-
    count_paths_helper(From, To, Count),
    assertz(path_count_memo(From, To, Count)).

count_paths_helper(Node, Node, 1) :- !.
count_paths_helper(From, To, Count) :-
    findall(Next, edge(From, Next), Nexts),
    maplist(count_paths_to(To), Nexts, Counts),
    sum_list(Counts, Count).

count_paths_to(To, From, Count) :-
    count_paths(From, To, Count).

% Count paths with required node visits
count_paths_with_requirements(From, To, Required, Count) :-
    count_paths_with_state(From, To, Required, [], Count).

% Count paths tracking which required nodes have been visited
count_paths_with_state(Node, Node, Required, Visited, Count) :-
    (   subset(Required, Visited)
    ->  Count = 1
    ;   Count = 0
    ), !.

count_paths_with_state(From, To, Required, Visited, Count) :-
    % Add current node to visited if it's required
    (   member(From, Required)
    ->  NewVisited = [From|Visited]
    ;   NewVisited = Visited
    ),
    
    % Find all next nodes and sum their path counts
    findall(Next, edge(From, Next), Nexts),
    maplist(count_paths_with_state_helper(To, Required, NewVisited), Nexts, Counts),
    sum_list(Counts, Count).

% Optimized Part 2 using DAG property (like the Python solution)
part2_optimized(Count) :-
    % Check which direction exists: fft->dac or dac->fft
    count_paths(fft, dac, FftToDac),
    count_paths(dac, fft, DacToFft),
    
    (   FftToDac > 0
    ->  % Path goes svr -> fft -> dac -> out
        count_paths(svr, fft, SvrToFft),
        count_paths(dac, out, DacToOut),
        Count is SvrToFft * FftToDac * DacToOut
    ;   DacToFft > 0
    ->  % Path goes svr -> dac -> fft -> out
        count_paths(svr, dac, SvrToDac),
        count_paths(fft, out, FftToOut),
        Count is SvrToDac * DacToFft * FftToOut
    ;   Count = 0
    ).

% Alternative: Find all actual paths (for small examples)
find_all_paths(From, To, Paths) :-
    findall(Path, path_between(From, To, [From], Path), Paths).

path_between(Node, Node, Visited, Path) :-
    reverse(Visited, Path).
path_between(From, To, Visited, Path) :-
    edge(From, Next),
    \+ member(Next, Visited),  % Avoid cycles
    path_between(Next, To, [Next|Visited], Path).

% Find paths with required nodes
find_paths_with_requirements(From, To, Required, Paths) :-
    find_all_paths(From, To, AllPaths),
    include(contains_all(Required), AllPaths, Paths).

contains_all(Required, Path) :-
    subset(Required, Path).

% Test predicates
test_example1 :-
    load_graph('example.txt'),
    part1(Count),
    format('Part 1 (example): ~w paths~n', [Count]).

test_example2 :-
    load_graph('example2.txt'),
    part2_optimized(Count),
    format('Part 2 (example): ~w paths~n', [Count]).

test_main :-
    load_graph('input.txt'),
    part1(Count1),
    format('Part 1: ~w paths~n', [Count1]),
    part2_optimized(Count2),
    format('Part 2: ~w paths~n', [Count2]).

% Debug: Show graph structure
show_graph :-
    forall(edge(From, To), format('~w -> ~w~n', [From, To])).

% Debug: Show some paths
show_example_paths :-
    load_graph('example.txt'),
    find_all_paths(you, out, Paths),
    length(Paths, Count),
    format('Found ~w paths:~n', [Count]),
    forall(member(Path, Paths), 
           (atomic_list_concat(Path, ' -> ', PathStr),
            format('  ~w~n', [PathStr]))).

count_paths_with_state_helper(To, Required, Visited, From, Count) :-
    count_paths_with_state(From, To, Required, Visited, Count).

% Utility: subset check
subset([], _).
subset([H|T], Set) :-
    member(H, Set),
    subset(T, Set).