% Day 8: Playground - Prolog solution for junction box connections
% Connect boxes using minimum spanning tree approach

:- use_module(library(lists)).

% Dynamic predicates for union-find structure
:- dynamic(parent/2).
:- dynamic(rank/2).

% Parse input file to get 3D coordinates
load_boxes(Filename, Boxes) :-
    open(Filename, read, Stream),
    read_lines(Stream, Lines),
    close(Stream),
    maplist(parse_coordinate, Lines, Boxes).

% Read all lines from stream
read_lines(Stream, Lines) :-
    read_line_to_codes(Stream, Codes),
    (   Codes == end_of_file
    ->  Lines = []
    ;   atom_codes(Line, Codes),
        Lines = [Line|RestLines],
        read_lines(Stream, RestLines)
    ).

% Parse coordinate line like "1,2,3"
parse_coordinate(Line, coord(X, Y, Z)) :-
    atomic_list_concat(Parts, ',', Line),
    Parts = [XAtom, YAtom, ZAtom],
    atom_number(XAtom, X),
    atom_number(YAtom, Y),
    atom_number(ZAtom, Z).

% Calculate Euclidean distance between two 3D points
distance(coord(X1, Y1, Z1), coord(X2, Y2, Z2), Dist) :-
    DX is X2 - X1,
    DY is Y2 - Y1,
    DZ is Z2 - Z1,
    Dist is sqrt(DX*DX + DY*DY + DZ*DZ).

% Generate all pairs of boxes with distances
generate_edges(Boxes, Edges) :-
    length(Boxes, N),
    N1 is N - 1,
    numlist(0, N1, Indices),
    findall(edge(Dist, I, J), 
            (member(I, Indices), 
             member(J, Indices), 
             I < J,
             nth0(I, Boxes, BoxI),
             nth0(J, Boxes, BoxJ),
             distance(BoxI, BoxJ, Dist)), 
            Edges).

% Initialize Union-Find structure
init_union_find(N) :-
    retractall(parent(_, _)),
    retractall(rank(_, _)),
    N1 is N - 1,
    numlist(0, N1, Indices),
    maplist(init_node, Indices).

init_node(I) :-
    assertz(parent(I, I)),
    assertz(rank(I, 0)).

% Find root with path compression
find_root(X, Root) :-
    parent(X, P),
    (   X == P
    ->  Root = X
    ;   find_root(P, Root),
        retract(parent(X, P)),
        assertz(parent(X, Root))
    ).

% Union two sets by rank
union_sets(X, Y) :-
    find_root(X, RootX),
    find_root(Y, RootY),
    (   RootX == RootY
    ->  fail  % Already in same set
    ;   rank(RootX, RankX),
        rank(RootY, RankY),
        (   RankX < RankY
        ->  retract(parent(RootX, RootX)),
            assertz(parent(RootX, RootY))
        ;   RankX > RankY
        ->  retract(parent(RootY, RootY)),
            assertz(parent(RootY, RootX))
        ;   % RankX == RankY
            retract(parent(RootY, RootY)),
            assertz(parent(RootY, RootX)),
            retract(rank(RootX, RankX)),
            NewRank is RankX + 1,
            assertz(rank(RootX, NewRank))
        )
    ).

% Count components in Union-Find structure
count_components(N, Count) :-
    N1 is N - 1,
    numlist(0, N1, Indices),
    findall(Root, (member(I, Indices), find_root(I, Root)), Roots),
    sort(Roots, UniqueRoots),
    length(UniqueRoots, Count).

% Get component sizes
get_component_sizes(N, Sizes) :-
    N1 is N - 1,
    numlist(0, N1, Indices),
    findall(Root, (member(I, Indices), find_root(I, Root)), Roots),
    msort(Roots, SortedRoots),
    group_consecutive(SortedRoots, Groups),
    maplist(length, Groups, Sizes).

% Group consecutive identical elements
group_consecutive([], []).
group_consecutive([H|T], [[H|Group]|RestGroups]) :-
    take_while_equal(H, T, Group, Rest),
    group_consecutive(Rest, RestGroups).

take_while_equal(_, [], [], []).
take_while_equal(X, [X|T], [X|Group], Rest) :-
    take_while_equal(X, T, Group, Rest).
take_while_equal(X, [Y|T], [], [Y|T]) :-
    X \== Y.

% Part 1: Connect 1000 edges and find product of 3 largest components
part1(Filename, NumEdges, Result) :-
    load_boxes(Filename, Boxes),
    length(Boxes, N),
    generate_edges(Boxes, UnsortedEdges),
    sort(UnsortedEdges, SortedEdges),
    
    init_union_find(N),
    connect_n_edges(SortedEdges, NumEdges, 0),
    
    get_component_sizes(N, AllSizes),
    sort(0, @>=, AllSizes, SortedSizes),  % Sort descending
    SortedSizes = [Size1, Size2, Size3|_],
    Result is Size1 * Size2 * Size3.

% Connect N edges using Union-Find
connect_n_edges(_, 0, _) :- !.
connect_n_edges([edge(_, I, J)|RestEdges], N, Connected) :-
    (   union_sets(I, J)
    ->  N1 is N - 1,
        Connected1 is Connected + 1
    ;   N1 = N,
        Connected1 = Connected
    ),
    connect_n_edges(RestEdges, N1, Connected1).
connect_n_edges([_|RestEdges], N, Connected) :-
    connect_n_edges(RestEdges, N, Connected).

% Part 2: Connect until one component, return product of X coordinates of last connection
part2(Filename, Result) :-
    load_boxes(Filename, Boxes),
    length(Boxes, N),
    generate_edges(Boxes, UnsortedEdges),
    sort(UnsortedEdges, SortedEdges),
    
    init_union_find(N),
    connect_until_one(SortedEdges, Boxes, N, Result).

% Connect edges until only one component remains
connect_until_one([edge(_, I, J)|RestEdges], Boxes, N, Result) :-
    (   union_sets(I, J)
    ->  count_components(N, Count),
        (   Count == 1
        ->  % Found the last connection
            nth0(I, Boxes, coord(XI, _, _)),
            nth0(J, Boxes, coord(XJ, _, _)),
            Result is XI * XJ
        ;   connect_until_one(RestEdges, Boxes, N, Result)
        )
    ;   connect_until_one(RestEdges, Boxes, N, Result)
    ).

% Test predicates
test_example :-
    part1('example.txt', 10, Result),
    format('Example Part 1 (10 edges): ~w~n', [Result]).

test_main_part1 :-
    part1('input.txt', 1000, Result),
    format('Part 1 (1000 edges): ~w~n', [Result]).

test_main_part2 :-
    part2('input.txt', Result),
    format('Part 2: ~w~n', [Result]).

% Debug: Show first few edges
show_edges(Filename, Count) :-
    load_boxes(Filename, Boxes),
    generate_edges(Boxes, UnsortedEdges),
    sort(UnsortedEdges, SortedEdges),
    take(Count, SortedEdges, FirstEdges),
    forall(member(edge(Dist, I, J), FirstEdges),
           format('Edge ~w-~w: distance ~w~n', [I, J, Dist])).

% Utility: take first N elements
take(0, _, []) :- !.
take(_, [], []) :- !.
take(N, [H|T], [H|Result]) :-
    N > 0,
    N1 is N - 1,
    take(N1, T, Result).