%%% -*- erlang -*-
%%%
%%% This file is part of couchapp released under the Apache 2 license. 
%%% See the NOTICE for more information.

-module(couchapp_core).
-author('Benoît Chesneau <benoitc@e-engura.org>').

-include("couchapp.hrl").

-export([run/1]).

run(["compile"]) ->
    ok;
run(["help"]) ->
    help(),
    ok; 
run(["version"]) ->
    ok = application:load(couchapp),
    version(),
    ok;
run(RawArgs) ->
    ok = application:load(couchapp),
   
    %% parse arguments
    Commands = parse_args(RawArgs),

    %% load couchbeam
    {ok, _} = couchbeam:start(),
    
    %% Initialize logging system
    couchapp_log:init(),

    ?INFO("commands ~p~n", [Commands]), 

    %% Determine the location of the rebar executable; important for pulling
    %% resources out of the escript
    couchapp_config:set_global(escript, filename:absname(escript:script_name())),
    ?DEBUG("Couchapp location: ~p\n", [couchapp_config:get_global(escript, undefined)]),

    %% Note the top-level directory for reference
    couchapp_config:set_global(base_dir, filename:absname(couchapp_util:get_cwd())),
 
    
    Server = couchbeam:server_connection(),
    Info = couchbeam:server_info(Server),
    io:format("server info: ~p~n", [Info]),
    ok.

parse_args(Args) ->
    OptSpecList = option_spec_list(),
    case getopt:parse(OptSpecList, Args) of
        {ok, {Options, NonOptArgs}} ->
            {ok, continue} = show_info_maybe_halt(Options, NonOptArgs),

            %% Set global variables based on getopt options
            set_global_flag(Options, verbose),
            set_global_flag(Options, force),
            
            %% Filter all the flags (i.e. strings of form key=value) from the
            %% command line arguments. What's left will be the commands to run.
            filter_flags(NonOptArgs, []);
        {error, {Reason, Data}} ->
            ?ERROR("Error: ~s ~p~n~n", [Reason, Data]),
            help(),
            halt(1)
    end.
    

%%
%% options accepted via getopt
%%
option_spec_list() ->
    [
     %% {Name, ShortOpt, LongOpt, ArgSpec, HelpMsg}
     {help,     $h, "help",       undefined, "Show the program options"},
     {commands, $c, "commands",   undefined, "Show available commands"},
     {verbose,  $v, "verbose",    undefined, "Be verbose about what gets done"},
     {force,    $f, "force",      undefined, "Force"},
     {version,  $V, "version",    undefined, "Show version information"}
    ].



%%
%% set global flag based on getopt option boolean value
%%
set_global_flag(Options, Flag) ->
    Value = case proplists:get_bool(Flag, Options) of
                true ->
                    "1";
                false ->
                    "0"
            end,
    couchapp_config:set_global(Flag, Value).

%%
%% show info and maybe halt execution
%%
show_info_maybe_halt(Opts, NonOptArgs) ->
    case proplists:get_bool(help, Opts) of
        true ->
            help(),
            halt(0);
        false ->
            case proplists:get_bool(commands, Opts) of
                true ->
                    commands(),
                    halt(0);
                false ->
                    case proplists:get_bool(version, Opts) of
                        true ->
                            version(),
                            halt(0);
                        false ->
                            case NonOptArgs of
                                [] ->
                                    ?CONSOLE("No command to run specified!~n",[]),
                                    help(),
                                    halt(1);
                                _ ->
                                    {ok, continue}
                            end
                    end
            end
    end.
help() ->
    OptSpecList = option_spec_list(),
    getopt:usage(OptSpecList, "couchapp",
                 "[...] <command,...>",
                 [{"command", "Command to run (e.g. push)"}]).
%%
%% print known commands
%%
commands() ->
    S = <<"
init                                 inititiliaze a couchapp
push        [options...] [dir] dest  push a document to couchdb                       
clone       [option] source dir      clone a document from couchdb
pushapps    [option] source dest     push all CouchApps in a folder 
                                     to couchdb
pushdocs    [option] source dest     push all docs in a folder to
                                     couchdb
generate    [option] func [dir] name generate a new couchapp or a
                                     function from a template
vendor                               install or update a vendor
            install [opts] dir src
            update  [opts] dir src
browse                               display the couchapp in the
                                     browser.

help                                 Show the program options
version                              Show version information
">>,
    io:put_chars(S),
    %% workaround to delay exit until all output is written
    timer:sleep(300).




%%
%% show version information and halt
%%
version() ->
    {ok, Vsn} = application:get_key(couchapp, vsn),
    ?CONSOLE("couchapp version: ~s\n", [Vsn]).


%%
%% Seperate all commands (single-words) from flags (key=value) and store
%% values into the rebar_config global storage.
%%
filter_flags([], Commands) ->
    lists:reverse(Commands);
filter_flags([Item | Rest], Commands) ->
    case string:tokens(Item, "=") of
        [Command] ->
            filter_flags(Rest, [Command | Commands]);
        [KeyStr, Value] ->
            Key = list_to_atom(KeyStr),
            couchapp_config:set_global(Key, Value),
            filter_flags(Rest, Commands);
        Other ->
            ?CONSOLE("Ignoring command line argument: ~p\n", [Other]),
            filter_flags(Rest, Commands)
    end. 