let schema_files = import.meta.globEager('@/task_plugins/*/*Schema.json');
let exported = {};

for (const file_name of Object.keys(schema_files)) {
  let added_export = schema_files[file_name].default;
  let component_name = file_name.split('/').at(-1).split('.json')[0];

  let exported_object = {};
  exported_object[component_name] = added_export;

  exported = {
    ...exported,
    ...exported_object,
  };
}

export default exported;
