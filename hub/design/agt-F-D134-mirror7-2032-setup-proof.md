# D134 mirror setup proof

The retained fixture creates `parent.clips` and `parent.config.clips` from the
same authored card. The new capture helper first asserts equal clip IDs and
full clip dictionaries, then aliases `config.clips` to that already-equal list
in the in-memory bundle. It never repairs an unequal authored mirror and never
touches the persisted Runtime document.

The exact test mutations now apply the same declaration/reference mutation to
both verified mirror views. The recipe reference-authority test keeps its real
first anchor publication and restart, then performs only its intentional echo
perturbation in the captured bundle because the test-local spike has no
production mirror writer for a second echo publication. Stable word IDs,
transcript pins, source clips, opaque values, grouping, and timing inputs are
otherwise untouched.

No source selection, text rebinding, clip/anchor deletion, clear, normalization,
guard, product, Runtime, client, generated, schema, or kit code changed.
