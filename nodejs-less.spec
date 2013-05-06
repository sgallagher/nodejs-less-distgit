%{?nodejs_find_provides_and_requires}

Name:           nodejs-less
Version:        1.3.3
Release:        4%{?dist}
Summary:        Less.js The dynamic stylesheet language

# cssmin.js is licensed under BSD license
# everything else is ASL 2.0
License:        ASL 2.0 and BSD

URL:            http://lesscss.org
Source0: http://registry.npmjs.org/less/-/less-1.3.3.tgz

# Since we're installing this in a global location, fix the require()
# calls to point there.
Patch0001: 0001-Require-include-files-from-the-default-location.patch

BuildArch:      noarch
BuildRequires:  nodejs-devel
Requires:       nodejs

Provides:  lessjs = %{version}-%{release}
Obsoletes: lessjs < 1.3.3-2

%description
LESS extends CSS with dynamic behavior such as variables, mixins, operations
and functions. LESS runs on both the client-side (Chrome, Safari, Firefox)
and server-side, with Node.js and Rhino.

%prep
%setup -q -n package

%patch0001 -p1

# Remove pre-built files from the dist/ directory
rm -f dist/*.js

# enable compression using ycssmin
%nodejs_fixdep ycssmin '~1.0.1'

%build
# Nothing to be built, we're just carrying around flat files

%check
make %{?_smp_mflags} test


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{nodejs_sitelib}/less
chmod a+x bin/lessc
cp -rp bin package.json lib/less/* %{buildroot}/%{nodejs_sitelib}/less

# Install /usr/bin/lessc
ln -s %{nodejs_sitelib}/less/bin/lessc \
      %{buildroot}%{_bindir}

%nodejs_symlink_deps

%files
%doc LICENSE README.md CHANGELOG.md CONTRIBUTING.md
%{_bindir}/lessc
%{nodejs_sitelib}/less


%changelog
* Mon May 06 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.3.3-4
- enable compression using ycssmin

* Wed Apr 10 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.3.3-3
- Fix BuildRequires to include nodejs-devel

* Tue Apr 09 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.3.3-2
- Rename package to nodejs-less

* Tue Apr 09 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.3.3-1
- Upgrade to new upstream release and switch to proper Node.js packaging
- New upstream release 1.3.3
    * Fix critical bug with mixin call if using multiple brackets
    * When using the filter contrast function, the function is passed through if
      the first argument is not a color
- New upstream release 1.3.2
    * browser and server url re-writing is now aligned to not re-write (previous
      lessc behaviour)
    * url-rewriting can be made to re-write to be relative to the entry file
      using the relative-urls option (less.relativeUrls option)
    * rootpath option can be used to add a base path to every url
    * Support mixin argument seperator of ';' so you can pass comma seperated
      values. e.g. .mixin(23px, 12px;);
    * Fix lots of problems with named arguments in corner cases, not behaving
      as expected
    * hsv, hsva, unit functions
    * fixed lots more bad error messages
    * fix @import-once to use the full path, not the relative one for
      determining if an import has been imported already
    * support :not(:nth-child(3))
    * mixin guards take units into account
    * support unicode descriptors (U+00A1-00A9)
    * support calling mixins with a stack when using & (broken in 1.3.1)
    * support @namespace and namespace combinators
    * when using %% with colour functions, take into account a colour is out of
      256
    * when doing maths with a %% do not divide by 100 and keep the unit
    * allow url to contain %% (e.g. %%20 for a space)
    * if a mixin guard stops execution a default mixin is not required
    * units are output in strings (use the unit function if you need to get the
      value without unit)
    * do not infinite recurse when mixins call mixins of the same name
    * fix issue on important on mixin calls
    * fix issue with multiple comments being confused
    * tolerate multiple semi-colons on rules
    * ignore subsequant @charset
    * syncImport option for node.js to read files syncronously
    * write the output directory if it is missing
    * change dependency on cssmin to ycssmin
    * lessc can load files over http
    * allow calling less.watch() in non dev mode
    * don't cache in dev mode
    * less files cope with query parameters better
    * sass debug statements are now chrome compatible
    * modifyVars function added to re-render with different root variables

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.3.1-4
- Unbundle cssmin.js from the sources
- Throw an error when --yui-compress is passed at the lessc command line
- Convert assorted %%prep actions into patches

* Wed Dec 19 2012 Matthias Runge <mrunge@redhat.com> - 1.3.1-3
- include LICENSE and README.md

* Wed Dec 19 2012 Matthias Runge <mrunge@redhat.com> - 1.3.1-2
- minor spec cleanup
- clear dist-dir
- license clearification

* Thu Dec 13 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.3.1-1
- Update to the 1.3.1 release
- Fix versioning bugs, get the tarball from a cleaner, tagged location

* Mon Sep 17 2012 Matthias Runge <mrunge@redhat.com> - 1.3.0-20120917git55d6e5a.1
- initial packaging
